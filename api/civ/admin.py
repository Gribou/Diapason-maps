from django.contrib import admin

from api.admin import AiracUpdateMixin
from .models import CivSchedule, AzbaArea, AzbaSchedule
from .tasks import download_azba_schedule


@admin.register(CivSchedule)
class CivScheduleAdmin(admin.ModelAdmin):
    model = CivSchedule
    list_display = ['label', 'reference']


class AzbaScheduleInline(admin.TabularInline):
    model = AzbaSchedule


@admin.register(AzbaArea)
class AzbaAreaAdmin(AiracUpdateMixin, admin.ModelAdmin):
    model = AzbaArea
    list_display = ['slug', 'label', 'airac',
                    'floor', 'ceiling', 'has_boundaries']
    search_fields = ['slug', 'label']
    list_filter = [('boundaries', admin.EmptyFieldListFilter), 'airac']
    inlines = [AzbaScheduleInline]

    def has_boundaries(self, obj):
        return obj.boundaries is not None and len(obj.boundaries) > 0
    has_boundaries.boolean = True
    has_boundaries.short_description = "Limites"

    def get_extra_buttons(self):
        return super().get_extra_buttons() + [{'title': "Télécharger programme", 'path': 'trigger-update-schedule/', 'method': self.trigger_update_schedule}]

    def trigger_update_schedule(self, request):
        return self.trigger_task(request, download_azba_schedule)


# @admin.register(AzbaKnownSchedule)
# class AzbaKnownScheduleAdmin(admin.ModelAdmin):
#     model = AzbaKnownSchedule
#     list_display = ['from_d', 'up_to']
