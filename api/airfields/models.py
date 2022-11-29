from django.db import models
from django.db.models import signals
from astral import Observer, sun

from api.signals import delete_old_file_on_model_update, delete_file_on_model_delete
from files.models import StaticFile


class Airfield(models.Model):
    name = models.CharField('Nom', max_length=250)
    icao_code = models.CharField('Code OACI', max_length=4, unique=True)
    latitude = models.IntegerField(
        'Latitude', default=0, help_text="(-1 si S) * (degrés * 3600 + minutes * 60 + secondes)")
    longitude = models.IntegerField(
        'Longitude', default=0, help_text="(-1 si W) * (degrés * 3600 + minutes * 60 + secondes)")
    elevation = models.IntegerField('Altitude ft', default=0)
    category = models.CharField(max_length=100, default=0)
    update_date = models.DateTimeField('Mise à jour', auto_now=True)
    files = models.ManyToManyField(
        StaticFile, related_name="airfields", blank=True)

    class Meta:
        verbose_name = 'Aérodrome'
        verbose_name_plural = 'Aérodromes'
        ordering = ['icao_code', 'name']

    def __str__(self):
        return '{} {}'.format(self.icao_code, self.name)

    @property
    def ephemeris(self):
        latitude_in_degrees = self.latitude / float(3600)
        longitude_in_degrees = self.longitude / float(3600)
        # elevation_in_meters = obj.elevation / 3.2808
        observer = Observer(latitude_in_degrees, longitude_in_degrees, 0)
        return sun.sun(observer)


class AirfieldMap(models.Model):
    airfield = models.ForeignKey(
        Airfield, related_name='maps', on_delete=models.CASCADE)
    airac = models.DateField('Cycle AIRAC')
    name = models.CharField('Nom', max_length=250)
    pdf = models.FileField('PDF', max_length=251, blank=True)
    update_date = models.DateTimeField('Mise à jour', auto_now=True)

    class Meta:
        verbose_name = 'Carte'
        verbose_name_plural = 'Cartes'
        ordering = ['-airac', 'airfield__icao_code', 'name']
        unique_together = ['name', 'airfield']

    def __str__(self):
        return '{} - {} ({})'.format(self.airfield.icao_code,
                                     self.name, self.airac)


FREQUENCY_TYPE = [('APP', 'Approche'), ('TWR', 'Tour'), ('GND', 'Sol'),
                  ('ATIS', 'ATIS'), ('AFIS', 'AFIS'), ('A/A', 'A/A')]


class AirfieldFrequency(models.Model):
    airfield = models.ForeignKey(
        Airfield, related_name='frequencies', on_delete=models.CASCADE)
    value = models.CharField('Fréquence', max_length=7)
    frequency_type = models.CharField(
        'Type de fréquence', max_length=4, choices=FREQUENCY_TYPE)
    airac = models.DateField('Cycle AIRAC')
    comments = models.CharField(
        "Observations", max_length=250, null=True, blank=True)
    update_date = models.DateTimeField('Mise à jour', auto_now=True)

    class Meta:
        verbose_name = 'Fréquence'
        verbose_name_plural = 'Fréquences'
        ordering = ['-airac', 'airfield__icao_code', 'frequency_type']

    def __str__(self):
        return self.airfield.icao_code


signals.post_delete.connect(
    delete_file_on_model_delete, sender=AirfieldMap, dispatch_uid="delete_map")
signals.pre_save.connect(delete_old_file_on_model_update,
                         sender=AirfieldMap, dispatch_uid="update_map")
