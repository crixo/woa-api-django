# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnamnesiProssima(models.Model):
    id_consulto = models.IntegerField(db_column='ID_consulto', blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    prima_volta = models.TextField(blank=True, null=True)  # This field type is a guess.
    tipologia = models.TextField(blank=True, null=True)  # This field type is a guess.
    localizzazione = models.TextField(blank=True, null=True)  # This field type is a guess.
    irradiazione = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodo_insorgenza = models.TextField(blank=True, null=True)  # This field type is a guess.
    durata = models.TextField(blank=True, null=True)  # This field type is a guess.
    familiarita = models.TextField(blank=True, null=True)  # This field type is a guess.
    altre_terapie = models.TextField(blank=True, null=True)  # This field type is a guess.
    varie = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'anamnesi_prossima'


class AnamnesiRemota(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    data = models.DateTimeField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'anamnesi_remota'


class Consulto(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    data = models.DateTimeField(blank=True, null=True)
    problema_iniziale = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'consulto'


class Esame(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    id_consulto = models.IntegerField(db_column='ID_consulto', blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    data = models.DateTimeField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.
    tipo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'esame'


class LkpAnamnesi(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lkp_anamnesi'


class LkpEsame(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lkp_esame'


class LkpProvincia(models.Model):
    sigla = models.TextField(blank=True, primary_key=True)  # This field type is a guess.
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lkp_provincia'


class Paziente(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    cognome = models.TextField(blank=True, null=True)  # This field type is a guess.
    nome = models.TextField(blank=True, null=True)  # This field type is a guess.
    professione = models.TextField(blank=True, null=True)  # This field type is a guess.
    indirizzo = models.TextField(blank=True, null=True)  # This field type is a guess.
    citta = models.TextField(blank=True, null=True)  # This field type is a guess.
    telefono = models.TextField(blank=True, null=True)  # This field type is a guess.
    cellulare = models.TextField(blank=True, null=True)  # This field type is a guess.
    prov = models.TextField(blank=True, null=True)  # This field type is a guess.
    cap = models.TextField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    data_nascita = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paziente'


class SinceTable(models.Model):
    table = models.CharField(max_length=255, blank=True, null=True)
    place = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'since_table'


class Trattamento(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    id_consulto = models.IntegerField(db_column='ID_consulto', blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    data = models.DateTimeField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'trattamento'


class Valutazione(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    id_consulto = models.IntegerField(db_column='ID_consulto', blank=True, null=False)  # Field name made lowercase.
    id_paziente = models.IntegerField(db_column='ID_paziente', blank=True, null=False)  # Field name made lowercase.
    strutturale = models.TextField(blank=True, null=True)  # This field type is a guess.
    cranio_sacrale = models.TextField(blank=True, null=True)  # This field type is a guess.
    ak_ortodontica = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'valutazione'
