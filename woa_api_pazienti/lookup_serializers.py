from rest_framework import serializers
from .models import LkpAnamnesi, LkpEsame, LkpProvincia


class LkpAnamnesiSerializer(serializers.ModelSerializer):
    class Meta:
        model = LkpAnamnesi
        fields = ("id", "descrizione")

class LkpEsameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LkpEsame
        fields = ("id", "descrizione")

class LkpProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LkpProvincia
        fields = ("sigla", "descrizione")