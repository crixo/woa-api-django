import logging


from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import pagination
from django.core.paginator import Paginator
from .models import Paziente
from .paziente_serializer import PazienteSerializer, PazienteFullSerializer

from .skip_take_pagination import SkipTakePagination


logger = logging.getLogger('paziente_views')


class ListPazienteView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer

class PazienteDetailView(generics.RetrieveAPIView):
    queryset = Paziente.objects.all()
    serializer_class = PazienteFullSerializer

class PazienteViewSet(viewsets.ModelViewSet):
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PazienteFullSerializer(instance)
        return Response(serializer.data)

#https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
# class CustomPagination(pagination.LimitOffsetPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'results': data
#         })

class PazientiPagedView(generics.GenericAPIView):
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer
    pagination_class = SkipTakePagination
    filter_backends = (filters.OrderingFilter,)
    #ordering_fields = ('username', 'email')
    ordering = ('cognome',)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#http://www.tomchristie.com/rest-framework-2-docs/api-guide/pagination
    # def page(self, request, version=None, skip=None, take=None):

    #     logger.debug(skip + '-' + take)
    #     queryset = Paziente.objects.all()
    #     paginator = Paginator(queryset, take)
    #     page = paginator.page(1)
    #     logger.debug(page)

    #     return page

