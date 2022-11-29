from django.db import models

CATEGORIES = [
    ('AIRFIELD', 'Aérodrome'),
    ('MAP', 'Carte'),
    ('SECTOR', 'Secteur'),
    ('PHONE', 'Téléphone'),
    ('RADIO', 'Radio'),
    ('FILE', 'Fichier'),
    ('AZBA', 'AZBA'),
    ('HOME', 'Accueil'),
    ('SCHEDULE', 'Horaires')
]


class Shortcut(models.Model):
    label = models.CharField(
        "Intitulé", max_length=100, null=False, blank=False)
    category = models.CharField(
        "Catégorie", choices=CATEGORIES, max_length=100)
    url = models.CharField(
        "Chemin", help_text="ex : /map", max_length=250, null=False, blank=False)

    class Meta:
        verbose_name = "Raccourci"
        verbose_name_plural = "Raccourcis"
        ordering = ['label']

    def __str__(self):
        return self.label


class HomePageItem(models.Model):
    rank = models.PositiveIntegerField("Ordre", default=0)
    shortcut = models.ForeignKey(
        Shortcut, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Elément de la page d'accueil"
        verbose_name_plural = "Page d'accueil"

    def __str__(self):
        return self.shortcut.label


class ToolbarItem(models.Model):
    rank = models.PositiveIntegerField("Ordre", default=0)
    shortcut = models.ForeignKey(
        Shortcut, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Elément de la barre d'outils"
        verbose_name_plural = "Barre d'outils"

    def __str__(self):
        return self.shortcut.label
