from django.contrib import admin

from .models import Shortcut, HomePageItem, ToolbarItem


@admin.register(Shortcut)
class ShortcutAdmin(admin.ModelAdmin):
    model = Shortcut
    list_display = ['label', 'category']


@admin.register(HomePageItem)
class HomePageItemAdmin(admin.ModelAdmin):
    model = HomePageItem
    list_display = ['rank', 'shortcut']


@admin.register(ToolbarItem)
class ToolbarItemAdmin(admin.ModelAdmin):
    model = ToolbarItem
    list_display = ['rank', 'shortcut']
