from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from .serializers import TelephoneCategorySerializer, TelephoneSerializer
from .models import TelephoneCategory, Telephone

# Create your views here.


class TelephoneViewSet(ReadOnlyModelViewSet):
    '''
    Annuaire de numéros téléphoniques abrégés
    Tenu à jour par l'administrateur
    '''
    serializer_class = TelephoneSerializer
    queryset = Telephone.objects.select_related('category')
    filter_backends = [SearchFilter]
    search_fields = ['name', 'telephone_number', '=category__name', 'alias']


class TelephoneCategoryViewSet(ReadOnlyModelViewSet):
    '''
    Catégories de l'annuaire
    Créées par l'administrateur
    '''
    serializer_class = TelephoneCategorySerializer
    queryset = TelephoneCategory.objects.prefetch_related('telephones')
