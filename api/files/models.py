from django.db import models
from django.db.models import signals
from django.core.validators import FileExtensionValidator

from api.signals import delete_old_file_on_model_update, delete_file_on_model_delete


class StaticFile(models.Model):
    label = models.CharField(
        'Intitulé', max_length=100, null=False, blank=False)
    pdf = models.FileField('Fichier PDF', blank=False, null=False, upload_to='files', validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])])
    rank = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = 'Fichier'
        verbose_name_plural = 'Fichiers'
        ordering = ['rank', 'label']

    def __str__(self):
        return self.label


class FileCategory(models.Model):
    label = models.CharField(
        "Intitulé", max_length=100, null=False, blank=False)
    rank = models.PositiveIntegerField("Ordre", default=0)
    files = models.ManyToManyField(
        StaticFile, related_name="categories", blank=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['rank', 'label']

    def __str__(self):
        return self.label


signals.post_delete.connect(
    delete_file_on_model_delete, sender=StaticFile, dispatch_uid="delete_file")
signals.pre_save.connect(delete_old_file_on_model_update,
                         sender=StaticFile, dispatch_uid="update_file")
