from rest_framework import generics
from .models import LkpAnamnesi, LkpEsame, LkpProvincia
from .lookup_serializers import LkpAnamnesiSerializer, LkpEsameSerializer, LkpProvinciaSerializer


class ListLkpAnamnesiView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = LkpAnamnesi.objects.all()
    serializer_class = LkpAnamnesiSerializer

class ListLkpEsameView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = LkpEsame.objects.all()
    serializer_class = LkpEsameSerializer

class ListLkpProvinciaView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = LkpProvincia.objects.all()
    serializer_class = LkpProvinciaSerializer