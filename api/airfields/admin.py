from django.contrib import admin

from api.admin import AiracUpdateMixin
from .models import AirfieldMap, Airfield, AirfieldFrequency


@admin.register(AirfieldMap)
class AirfieldMapAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = AirfieldMap
    list_display = ['airac', 'airfield', 'name', 'pdf', 'update_date']
    search_fields = ('airac', 'name', 'airfield__name', 'airfield__icao_code')
    ordering = ['airac', 'airfield', 'name']


@admin.register(Airfield)
class AirfieldAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = Airfield
    list_display = ['icao_code', 'name', 'category', 'update_date']
    search_fields = ('icao_code', 'name', 'category')
    ordering = ['icao_code', 'name']
    filter_horizontal = ['files']


@admin.register(AirfieldFrequency)
class AirfieldFrequencyAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = AirfieldFrequency
    list_display = ['airac', 'airfield',
                    'value', 'frequency_type', 'comments', 'update_date']
    search_fields = ['airfield__icao_code', 'frequency_type']
