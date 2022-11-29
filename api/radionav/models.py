from tabnanny import verbose
from django.db import models


class RadioNavType(models.Model):
    label = models.CharField(
        "Type", null=False, blank=False, max_length=25, unique=True)

    class Meta:
        ordering = ['label']
        verbose_name = "Type de moyen radio"
        verbose_name_plural = "Types de moyen radio"

    def __str__(self):
        return self.label


class PrefetchingStationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related("types")


class RadioNavStation(models.Model):
    objects = PrefetchingStationManager()
    short_name = models.CharField(
        "Identifiant", null=False, blank=False, max_length=10, unique=True)
    long_name = models.CharField(
        "Nom complet", null=True, blank=True, max_length=250)
    types = models.ManyToManyField(RadioNavType, related_name="stations")
    frequency = models.CharField(
        "Fréquence", null=True, blank=True, max_length=250)
    latitude = models.IntegerField(
        'Latitude', default=0, help_text="(-1 si S) * (degrés * 3600 + minutes * 60 + secondes)")
    longitude = models.IntegerField(
        'Longitude', default=0, help_text="(-1 si W) * (degrés * 3600 + minutes * 60 + secondes)")
    range = models.CharField("Portée", null=True, blank=True, max_length=250)
    airac = models.DateField('Cycle AIRAC')

    class Meta:
        ordering = ['short_name']
        verbose_name = "Moyens radio"
        verbose_name_plural = "Moyens radio"

    def __str__(self):
        return self.short_name
