from rest_framework import serializers

from .models import FileCategory, StaticFile


class StaticFileSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    global_search = serializers.SerializerMethodField()

    class Meta:
        model = StaticFile
        fields = ['pk', 'label', 'pdf', 'categories', 'global_search']

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        try:
            return {
                "title": obj.label,
                "url": self.context['request'].build_absolute_uri(obj.pdf.url)
            }
        except:
            pass


class FileCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FileCategory
        fields = ['label', 'files']

    def to_representation(self, instance):
        '''show nested object on read, expect pk on write'''
        response = super().to_representation(instance)
        response['files'] = StaticFileSerializer(
            instance.files.all(), many=True, context=self.context).data
        return response
