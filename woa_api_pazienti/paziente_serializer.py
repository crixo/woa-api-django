from rest_framework import serializers
from .models import Paziente, Consulto

class ConsultoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulto
        fields = ('id', 'id_paziente', 'data', 'problema_iniziale')


class PazienteSerializer(serializers.ModelSerializer):
    #https://stackoverflow.com/questions/22958058/how-to-change-field-name-in-django-rest-framework
    #https://wsvincent.com/django-rest-framework-changing-field-names/
    dataDiNascita = serializers.CharField(source='data_nascita')
    class Meta:
        model = Paziente
        fields = ("id", "nome", "cognome", "dataDiNascita")
    def get_alternate_data_nascita(self, obj):
        return 'dataDiNascita'

class PazienteFullSerializer(serializers.ModelSerializer):
    #https://stackoverflow.com/questions/22958058/how-to-change-field-name-in-django-rest-framework
    #https://wsvincent.com/django-rest-framework-changing-field-names/
    dataDiNascita = serializers.CharField(source='data_nascita')
    consulti = ConsultoSerializer(many=True, source='consulto_set')
    class Meta:
        model = Paziente
        fields = ("id", "nome", "cognome", "dataDiNascita", "consulti")
    def get_alternate_data_nascita(self, obj):
        return 'dataDiNascita'