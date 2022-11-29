import traceback
from rest_framework import serializers
import json

from .models import KMLMap, MapLayer, LayerFolder


class MapLayerSerializer(serializers.ModelSerializer):
    tiles_url = serializers.SerializerMethodField()

    class Meta:
        model = MapLayer
        fields = ['label', 'depth', 'metadata',
                  'tiles_url', 'slug', 'mbtiles_file', 'format', 'style']
        extra_kwargs = {
            'mbtiles_file': {'write_only': True},
            'zip_file': {'write_only': True},
            'metadata': {'read_only': True},
        }

    def get_tiles_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.tiles_url)


class LayerFolderSerializer(serializers.ModelSerializer):
    layers = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = LayerFolder
        fields = ['pk', 'label', 'layers', 'children']

    def get_layers(self, obj):
        return MapLayerSerializer(obj.layers.filter(metadata__isnull=False), many=True, context=self.context).data

    def get_children(self, obj):
        # serialize child folders with LayerFolderSerializer
        return self.__class__(obj.children, many=True, context=self.context).data


class KMLMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = KMLMap
        fields = ['pk', 'label', 'kml_file']
