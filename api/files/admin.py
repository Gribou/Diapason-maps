from django.contrib import admin

from .models import StaticFile, FileCategory


@admin.register(StaticFile)
class StaticFileAdmin(admin.ModelAdmin):
    model = StaticFile
    list_display = ('label', 'pdf')


@admin.register(FileCategory)
class FileCategoryAdmin(admin.ModelAdmin):
    model = FileCategory
    list_display = ('label', 'file_count')
    filter_horizontal = ['files']

    def file_count(self, obj):
        return obj.files.count()
    file_count.short_description = 'Nb Fichiers'
