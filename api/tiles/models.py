from django.db import models
from django.conf import settings
from django.dispatch.dispatcher import receiver
from django.db.models import signals
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from treenode.models import TreeNodeModel
import os
import shutil

from .tasks import make_tiles_from_mbtiles, make_tiles_from_zip


class MapLayer(models.Model):
    label = models.CharField("Intitulé", null=False,
                             blank=False, max_length=25)
    slug = models.SlugField("Identifiant", null=False,
                            blank=False, unique=True)
    depth = models.PositiveIntegerField("Profondeur", default=0)
    metadata = models.JSONField("Métadonnées", null=True, blank=True)
    mbtiles_file = models.FileField(
        "Fichier MBTiles", upload_to="import/", null=True,
        blank=True, help_text="Importer un nouveau fichier MBTiles pour générer de nouvelles tuiles", validators=[
            FileExtensionValidator(allowed_extensions=['mbtiles'])])
    zip_file = models.FileField(
        "Fichier Zip", upload_to="import/", null=True, blank=True,
        help_text="Importer un nouveau fichier ZIP contenant l'arborescence des tuiles (Z/X/Y.ext où Z est le niveau de zoom et ext vaut png ou pbf). Cette arborescence doit être à la racine du ZIP.", validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    style = models.JSONField('Données de style', null=True, blank=True,
                             help_text="Si les tuiles sont vectorielles (PBF), importer ici les styles au format JSON")
    show_by_default = models.BooleanField(
        "Afficher par défault", default=False)

    class Meta:
        ordering = ['-depth', 'label']
        verbose_name = "Calque"
        verbose_name_plural = "Calques"

    def __str__(self):
        return self.label

    def has_tiles(self):
        return default_storage.exists("tiles/{}/metadata.json".format(self.slug))

    @property
    def format(self):
        if self.metadata:
            return self.metadata.get("format", None)

    @property
    def tiles_url(self):
        format = self.format
        if format:
            return self.has_tiles() and settings.MEDIA_URL + "tiles/{}/$Z/$X/$Y.{}".format(self.slug, format)
    tiles_url.fget.short_description = "URL"


@receiver(signals.pre_save, sender=MapLayer, dispatch_uid="move_tile_folder_on_layer_update")
def move_tile_folder_on_layer_update(sender, instance, **kwargs):
    if instance.pk is not None:
        previous = MapLayer.objects.filter(pk=instance.pk).first()
        if previous is not None and previous.slug != instance.slug and previous.has_tiles():
            previous_path = default_storage.path(
                os.path.join("tiles", previous.slug))
            new_path = default_storage.path(
                os.path.join("tiles", instance.slug))
            os.rename(previous_path, new_path)


@receiver(signals.post_save, sender=MapLayer, dispatch_uid="update_tiles_on_layer_update")
def update_tiles_for_layer(sender, instance, **kwargs):
    if instance.mbtiles_file and os.path.isfile(instance.mbtiles_file.path):
        make_tiles_from_mbtiles.delay(instance.pk)
    elif instance.zip_file and os.path.isfile(instance.zip_file.path):
        make_tiles_from_zip(instance.pk)


@receiver(signals.pre_delete, sender=MapLayer, dispatch_uid="delete_tiles_on_layer_delete")
def delete_tiles_on_layer_delete(sender, instance, **kwargs):
    if instance.mbtiles_file is not None:
        instance.mbtiles_file.delete(save=False)
    if instance.zip_file is not None:
        instance.zip_file.delete(save=False)
    if instance.has_tiles():
        shutil.rmtree(default_storage.path(
            os.path.join("tiles", instance.slug)))


class LayerFolder(TreeNodeModel):
    treenode_display_field = 'label'
    label = models.CharField(
        "Intitulé", max_length=100, null=False, blank=False)
    layers = models.ManyToManyField(
        MapLayer, related_name="folders", blank=True)

    class Meta:
        verbose_name = "Groupe de calques"
        verbose_name_plural = "Groupes de calques"


class KMLMap(models.Model):
    label = models.CharField("Intitulé", null=False,
                             blank=False, max_length=25)
    kml_file = models.FileField(
        "Fichier KML", upload_to="kml/", validators=[FileExtensionValidator(allowed_extensions=['kml'])])

    class Meta:
        verbose_name = "Carte KML"
        verbose_name_plural = "Cartes KML"
        ordering = ['label']


class KMLMapAsset(models.Model):
    map = models.ForeignKey(
        KMLMap, on_delete=models.CASCADE, null=False, blank=False)
    file = models.FileField(
        "Fichier", upload_to="kml/",
        null=False, blank=False, help_text="Fichier nécessaire à la carte parente : icône, etc. Utiliser l'URL (ex : /media/kml/mon-fichier.png) de ce fichier telle quelle dans votre KML.")
