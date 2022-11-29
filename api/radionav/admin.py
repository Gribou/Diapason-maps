from django.contrib import admin

from api.admin import AiracUpdateMixin
from .models import RadioNavStation


@admin.register(RadioNavStation)
class RadioNavStationAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = RadioNavStation
    list_display = ['short_name', 'long_name', 'get_types', 'airac']

    def get_types(self, obj):
        return " ".join([t.label for t in obj.types.all()])
