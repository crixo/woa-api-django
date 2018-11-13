from rest_framework import serializers
from .models import Paziente


class PazienteSerializer(serializers.ModelSerializer):
    #https://stackoverflow.com/questions/22958058/how-to-change-field-name-in-django-rest-framework
    #https://wsvincent.com/django-rest-framework-changing-field-names/
    dataDiNascita = serializers.CharField(source='data_nascita')
    class Meta:
        model = Paziente
        fields = ("id", "nome", "cognome", "dataDiNascita")
    def get_alternate_data_nascita(self, obj):
        return 'dataDiNascita'