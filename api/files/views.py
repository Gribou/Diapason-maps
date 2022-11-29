from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.parsers import MultiPartParser

from .serializers import FileCategorySerializer, StaticFileSerializer
from .models import StaticFile, FileCategory


class StaticFileViewSet(ModelViewSet):
    '''
    Fichiers PDF personnalisés
    Peuvent ensuite être associés à un secteur, une catégorie et/ou un aérodrome
    Mise à jour par API possible avec un compte utilisateur adapté (POST/PUT/DELETE FormData)
    '''
    serializer_class = StaticFileSerializer
    queryset = StaticFile.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['label', "categories__label"]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    parser_classes = [MultiPartParser]


class FileCategoryViewSet(ModelViewSet):
    '''
    Organisation des fichiers PDF personnalisés
    Mise à jour par API possible avec un compte utilisateur adapté (POST/PUT/DELETE JSON)
    '''
    serializer_class = FileCategorySerializer
    queryset = FileCategory.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
