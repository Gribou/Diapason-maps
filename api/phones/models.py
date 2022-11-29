from django.db import models


class TelephoneCategory(models.Model):
    name = models.CharField('Nom', max_length=256)
    rank = models.IntegerField('Rang', default=0)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['rank', 'name']

    def __str__(self):
        return self.name


class Telephone(models.Model):
    name = models.CharField('Nom', max_length=256)
    category = models.ForeignKey(TelephoneCategory, related_name='telephones',
                                 related_query_name='telephone', on_delete=models.SET_NULL, null=True)
    telephone_number = models.CharField('Numéro abrégé', max_length=7)
    isExterior = models.BooleanField('Numéro extérieur', default=True)
    isCDS = models.BooleanField(
        'Montrer CDS', default=True, null=True, blank=True)
    isW = models.BooleanField('Montrer Zone Ouest',
                              default=True, null=True, blank=True)
    isE = models.BooleanField(
        'Montrer Zone Est', default=True, null=True, blank=True)
    alias = models.CharField('Alias', max_length=256,
                             default=None, null=True, blank=True)
    update_date = models.DateTimeField('Mise à jour', auto_now=True)

    class Meta:
        verbose_name = 'Téléphone'
        verbose_name_plural = 'Téléphones'
        ordering = ['category', 'name', 'telephone_number']

    def __str__(self):
        return self.name
