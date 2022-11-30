from django.db import models
from django.utils import timezone
from datetime import timedelta

from airfields.models import Airfield


class CivSchedule(models.Model):
    label = models.CharField("Intitulé", max_length=100)
    reference = models.ForeignKey(
        Airfield, null=True, blank=True, on_delete=models.SET_NULL, help_text="Aérodrome de référence pour le calcul de la nuit aéronautique")
    opening_min = models.PositiveIntegerField(
        "Ouverture au plus tôt", default=9, help_text="(heure locale)")
    opening_max = models.PositiveIntegerField(
        "Ouverture au plus tard", default=9, help_text="(heure locale)")
    closing_min = models.PositiveIntegerField(
        "Fermeture au plus tôt", default=19, help_text="(heure locale)")
    closing_max = models.PositiveIntegerField(
        "Fermeture au plus tard", default=21, help_text="(heure locale)")

    class Meta:
        verbose_name = "Horaires CIV"

    @property
    def open_at(self):
        # sunrise - 30 min at reference airfield
        if self.reference is None:
            return self._make_datetime(self.opening_min)
        else:
            local_sunrise = timezone.localtime(
                self.reference.ephemeris['sunrise'])
            return min(max(local_sunrise - timedelta(minutes=30),
                           self._make_datetime(self.opening_min)),
                       self._make_datetime(self.opening_max))

    @property
    def closed_at(self):
        # sunset + 30 min at reference airfield
        if self.reference is None:
            return self._make_datetime(self.closing_min)
        else:
            local_sunset = timezone.localtime(
                self.reference.ephemeris['sunset'])
            return min(max(local_sunset + timedelta(minutes=30),
                           self._make_datetime(self.closing_min)),
                       self._make_datetime(self.closing_max))

    @property
    def is_open(self):
        now = timezone.localtime(timezone.now())
        return now > self.open_at and now < self.closed_at

    def _make_datetime(self, hour):
        return timezone.localtime(timezone.now()).replace(hour=hour, minute=0, second=0, microsecond=0)


class AzbaArea(models.Model):
    label = models.CharField("Intitulé", max_length=25,
                             null=False, blank=False)
    slug = models.CharField("Identifiant", max_length=25,
                            null=False, blank=False)
    airac = models.DateField('Cycle AIRAC')
    ceiling = models.CharField("Plafond", null=True, blank=True, max_length=25)
    floor = models.CharField("Plancher", null=True, blank=True, max_length=25)
    boundaries = models.JSONField("Limites", null=True, blank=True)

    class Meta:
        verbose_name = "Zone réglementée"
        verbose_name_plural = "Zones réglementées"
        ordering = ['-airac', 'label']


class AzbaSchedule(models.Model):
    azba = models.ForeignKey(
        AzbaArea, related_name="schedules", on_delete=models.CASCADE)
    activation_time = models.DateTimeField("Début d'activité")
    deactivation_time = models.DateTimeField("Fin d'activité")

    class Meta:
        verbose_name = "Activité AZBA"
        verbose_name_plural = "Planification AZBA"
        ordering = ["activation_time", "-deactivation_time"]


class AzbaKnownSchedule(models.Model):
    up_to = models.DateTimeField(null=False, blank=False)
    from_d = models.DateTimeField(null=False, blank=False)

    class Meta:
        ordering = ["-up_to"]
