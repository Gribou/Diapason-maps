from django.db import models

from files.models import StaticFile


class ControlCenter(models.Model):
    name = models.CharField('Centre de contrôle', max_length=256)
    rank = models.PositiveIntegerField('Ordre', default=0)

    class Meta:
        verbose_name = 'Centre de contrôle'
        verbose_name_plural = 'Centres de contrôle'
        ordering = ['rank', 'name']

    def __str__(self):
        return self.name


class Antenna(models.Model):
    name = models.CharField('Nom', max_length=256)
    latitude = models.IntegerField(
        'Latitude', default=0, help_text="(-1 si S) * (degrés * 3600 + minutes * 60 + secondes)")
    longitude = models.IntegerField(
        'Longitude', default=0, help_text="(-1 si W) * (degrés * 3600 + minutes * 60 + secondes)")

    class Meta:
        verbose_name = 'Antenne Radio'
        verbose_name_plural = 'Antennes Radio'

    def __str__(self):
        return '{}'.format(self.name)


FREQUENCY_TYPE = [('V', 'VHF'), ('U', 'UHF')]


class SectorFrequency(models.Model):
    frequency = models.CharField('Fréquence', max_length=7)
    frequency_type = models.CharField(
        'Type de fréquence', max_length=3, choices=FREQUENCY_TYPE)
    is833 = models.BooleanField('Est 8.33kHz', default=True)
    airac = models.DateField('Cycle AIRAC')

    class Meta:
        verbose_name = 'Fréquence'
        verbose_name_plural = 'Fréquences'
        ordering = ['frequency']

    def __str__(self):
        return self.frequency


class Sector(models.Model):
    name = models.CharField('Nom', max_length=10)
    control_center = models.ForeignKey(
        ControlCenter, related_name='sectors', on_delete=models.CASCADE, null=True, blank=True)
    frequencies = models.ManyToManyField(
        SectorFrequency, related_name='sectors', blank=True, default=None)
    main_antennas = models.ManyToManyField(
        Antenna, related_name='main_sectors', blank=True, default=None, verbose_name="Antennes principales")
    alternate_antennas = models.ManyToManyField(
        Antenna, related_name='alternate_sectors', blank=True, default=None, verbose_name="Antennes secours")
    hidden = models.BooleanField('Ne pas montrer', default=False)
    update_date = models.DateTimeField('Mise à jour', auto_now=True)
    files = models.ManyToManyField(
        StaticFile, related_name="sectors", blank=True)

    class Meta:
        verbose_name = 'Secteur'
        verbose_name_plural = 'Secteurs'
        ordering = ['control_center', 'name']

    def __str__(self):
        return 'Secteur {}'.format(self.name)


class SectorPart(models.Model):
    sector = models.ForeignKey(
        Sector, related_name="parts", on_delete=models.CASCADE)
    airac = models.DateField('Cycle AIRAC')
    ceiling = models.CharField("Plafond", null=True, blank=True, max_length=25)
    floor = models.CharField("Plancher", null=False,
                             blank=False, max_length=25)
    boundaries = models.JSONField("Limites", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Morceau de secteur'
        verbose_name = 'Morceaux de secteur'
