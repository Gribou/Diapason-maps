from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField, SerializerMethodField)
from django.urls import reverse

from .models import TelephoneCategory, Telephone


class TelephoneSerializer(ModelSerializer):
    category = StringRelatedField()
    global_search = SerializerMethodField()

    class Meta:
        model = Telephone
        fields = ['name', 'category', 'telephone_number',
                  'isExterior', 'isCDS', 'isW', 'isE', 'alias', 'global_search']

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        index_url = self.context['request'].build_absolute_uri(reverse("home"))
        return {
            "title": obj.name,
            "subtitle": obj.telephone_number,
            "url": "{}telephones/".format(index_url)
        }


class TelephoneCategorySerializer(ModelSerializer):
    telephones = TelephoneSerializer(many=True)

    class Meta:
        model = TelephoneCategory
        fields = ['name', 'rank', 'telephones']
