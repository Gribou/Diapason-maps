from django.contrib import admin
from api.admin import AiracUpdateMixin
from .models import Antenna, ControlCenter, Sector, SectorPart, SectorFrequency


@admin.register(Antenna)
class AntennaAdmin(admin.ModelAdmin):
    model = Antenna
    list_display = ['name', 'latitude', 'longitude']
    ordering = ['name']


@admin.register(ControlCenter)
class ControlCenterAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = ControlCenter
    list_display = ['name', 'rank']
    search_fields = ['name']
    ordering = ['rank', 'name']


@admin.register(SectorFrequency)
class SectorFrequencyAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = SectorFrequency
    list_display = ['frequency', 'frequency_type', 'is833', 'airac']
    search_fields = ['frequency']
    ordering = ['frequency']


class SectorPartInline(admin.TabularInline):
    model = SectorPart


@admin.register(Sector)
class SectorAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = Sector
    list_display = ['name', 'control_center',
                    'get_frequencies', 'has_boundaries', 'get_main_antennas', 'get_alternate_antennas', 'hidden']
    search_fields = ['name', 'control_center__name']
    list_filter = (
        ("parts", admin.EmptyFieldListFilter),
        "control_center",
    )
    inlines = [SectorPartInline]
    ordering = ['control_center__name', 'name']
    filter_horizontal = ['frequencies', 'files',
                         'main_antennas', 'alternate_antennas']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('control_center')\
            .prefetch_related('files', 'frequencies', 'parts', 'main_antennas', 'alternate_antennas',)

    def get_frequencies(self, obj):
        return ' '.join([str(f.frequency) for f in obj.frequencies.all() if f is not None and f.frequency_type == "V"])
    get_frequencies.short_description = "Fréquences VHF"

    def has_boundaries(self, obj):
        return obj.parts.exists()
    has_boundaries.boolean = True
    has_boundaries.short_description = "Limites"

    def get_main_antennas(self, obj):
        return ' + '.join([a.name for a in obj.main_antennas.all()])
    get_main_antennas.short_description = "Antennes principales"

    def get_alternate_antennas(self, obj):
        return ' + '.join([a.name for a in obj.alternate_antennas.all()])
    get_alternate_antennas.short_description = "Antennes secours"
