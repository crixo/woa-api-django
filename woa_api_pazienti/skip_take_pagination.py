# coding: utf-8
"""
Pagination serializers determine the structure of the output that should
be used for paginated responses.
"""
from __future__ import unicode_literals


import logging

from base64 import b64decode, b64encode
from collections import OrderedDict, namedtuple

from django.core.paginator import InvalidPage
from django.core.paginator import Paginator as DjangoPaginator
from django.template import loader
from django.utils import six
from django.utils.encoding import force_text
#from django.utils.six.moves.urllib import parse as urlparse
from django.utils.translation import ugettext_lazy as _

from rest_framework.compat import coreapi, coreschema
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.pagination import BasePagination

_logger = logging.getLogger('skip-take-pagination')

def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


def _divide_with_ceil(a, b):
    """
    Returns 'a' divided by 'b', with any remainder rounded up.
    """
    if a % b:
        return (a // b) + 1

    return a // b


def _get_displayed_page_numbers(current, final):
    """
    This utility function determines a list of page numbers to display.
    This gives us a nice contextually relevant set of page numbers.
    For example:
    current=14, final=16 -> [1, None, 13, 14, 15, 16]
    This implementation gives one page to each side of the cursor,
    or two pages to the side when the cursor is at the edge, then
    ensures that any breaks between non-continuous page numbers never
    remove only a single page.
    For an alternative implementation which gives two pages to each side of
    the cursor, eg. as in GitHub issue list pagination, see:
    https://gist.github.com/tomchristie/321140cebb1c4a558b15
    """
    assert current >= 1
    assert final >= current

    if final <= 5:
        return list(range(1, final + 1))

    # We always include the first two pages, last two pages, and
    # two pages either side of the current page.
    included = {1, current - 1, current, current + 1, final}

    # If the break would only exclude a single page number then we
    # may as well include the page number instead of the break.
    if current <= 4:
        included.add(2)
        included.add(3)
    if current >= final - 3:
        included.add(final - 1)
        included.add(final - 2)

    # Now sort the page numbers and drop anything outside the limits.
    included = [
        idx for idx in sorted(list(included))
        if 0 < idx <= final
    ]

    # Finally insert any `...` breaks
    if current > 4:
        included.insert(1, None)
    if current < final - 3:
        included.insert(len(included) - 1, None)
    return included


def _get_page_links(page_numbers, current, url_func):
    """
    Given a list of page numbers and `None` page breaks,
    return a list of `PageLink` objects.
    """
    page_links = []
    for page_number in page_numbers:
        if page_number is None:
            page_link = PAGE_BREAK
        else:
            page_link = PageLink(
                url=url_func(page_number),
                number=page_number,
                is_active=(page_number == current),
                is_break=False
            )
        page_links.append(page_link)
    return page_links


def _reverse_ordering(ordering_tuple):
    """
    Given an order_by tuple such as `('-created', 'uuid')` reverse the
    ordering and return a new tuple, eg. `('created', '-uuid')`.
    """
    def invert(x):
        return x[1:] if x.startswith('-') else '-' + x

    return tuple([invert(item) for item in ordering_tuple])


Cursor = namedtuple('Cursor', ['offset', 'reverse', 'position'])
PageLink = namedtuple('PageLink', ['url', 'number', 'is_active', 'is_break'])

PAGE_BREAK = PageLink(url=None, number=None, is_active=False, is_break=True)

class SkipTakePagination(BasePagination):
    """
    A limit/offset based style. For example:
    http://api.example.org/accounts/?limit=100
    http://api.example.org/accounts/?offset=400&limit=100
    """
    default_limit = api_settings.PAGE_SIZE
    limit_query_param = 'limit'
    limit_query_description = _('Number of results to return per page.')
    offset_query_param = 'offset'
    offset_query_description = _('The initial index from which to return the results.')
    max_limit = None
    template = 'rest_framework/pagination/numbers.html'

    def append_querystring(self, link):
        query_string = self.request.GET.urlencode()
        if query_string:
            link += '?' + query_string
        return link

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_limit(self, request):
        _logger.debug(request)
        _logger.debug(request.path)
        segments = request.path.split('/')
        _logger.debug('limit:'+segments[-1])
        if self.limit_query_param:
            try:
                return _positive_int(
                    segments[-1],#request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

    def get_offset(self, request):
        segments = request.path.split('/')
        _logger.debug('offset:'+segments[-2])
        try:
            return _positive_int(
                segments[-2]
                #request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError):
            return 0

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        #return replace_query_param(url, self.offset_query_param, offset)
        segments = self.request.path.split('/')
        _logger.debug(segments)
        segments[-2] = str(offset)
        segments[-1] = str(self.limit)
        _logger.debug(self.request.GET.urlencode())
        link = self.request.build_absolute_uri('/'.join(segments))
        return self.append_querystring(link)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        # if self.offset - self.limit <= 0:
        #     return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        #return replace_query_param(url, self.offset_query_param, offset)
        segments = self.request.path.split('/')
        #_logger.debug('get_previous_link'+segments)
        segments[-2] = str(offset)
        segments[-1] = str(self.limit)
        _logger.debug(self.request.GET.urlencode())
        link = self.request.build_absolute_uri('/'.join(segments))
        _logger.debug('get_previous_link'+link)
        return self.append_querystring(link)

    def get_html_context(self):
        base_url = self.request.build_absolute_uri()

        if self.limit:
            current = _divide_with_ceil(self.offset, self.limit) + 1

            # The number of pages is a little bit fiddly.
            # We need to sum both the number of pages from current offset to end
            # plus the number of pages up to the current offset.
            # When offset is not strictly divisible by the limit then we may
            # end up introducing an extra page as an artifact.
            final = (
                _divide_with_ceil(self.count - self.offset, self.limit) +
                _divide_with_ceil(self.offset, self.limit)
            )

            if final < 1:
                final = 1
        else:
            current = 1
            final = 1

        if current > final:
            current = final

        def page_number_to_url(page_number):
            if page_number == 1:
                #return remove_query_param(base_url, self.offset_query_param)
                segments = self.request.path.split('/')
                segments[-2] = str(0)
                segments[-1] = str(self.limit)
                link = self.request.build_absolute_uri('/'.join(segments))
                return self.append_querystring(link)
            else:
                offset = self.offset + ((page_number - current) * self.limit)
                #return replace_query_param(base_url, self.offset_query_param, offset)
                segments = self.request.path.split('/')
                segments[-2] = str(offset)
                segments[-1] = str(self.limit)
                link = self.request.build_absolute_uri('/'.join(segments))
                return self.append_querystring(link)

        page_numbers = _get_displayed_page_numbers(current, final)
        page_links = _get_page_links(page_numbers, current, page_number_to_url)

        return {
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link(),
            'page_links': page_links
        }

    def to_html(self):
        template = loader.get_template(self.template)
        context = self.get_html_context()
        return template.render(context)

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.limit_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Limit',
                    description=force_text(self.limit_query_description)
                )
            ),
            coreapi.Field(
                name=self.offset_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Offset',
                    description=force_text(self.offset_query_description)
                )
            )
        ]

    def get_count(self, queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)