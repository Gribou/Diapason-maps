from rest_framework import serializers

from .models import Shortcut, HomePageItem, ToolbarItem


class ShortcutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shortcut
        fields = ['label', 'category', 'url']


class HomePageItemSerializer(serializers.ModelSerializer):
    shortcut = ShortcutSerializer()

    class Meta:
        model = HomePageItem
        fields = ['shortcut']


class ToolbarItemSerializer(serializers.ModelSerializer):
    shortcut = ShortcutSerializer()

    class Meta:
        model = ToolbarItem
        fields = ['shortcut']
