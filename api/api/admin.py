from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, path
from django.utils.safestring import mark_safe
from django.contrib import admin
from constance import config

from .tasks import download_last_airac, pull_from_diapason


class ExtraButtonsMixin:
    change_list_template = "api/admin/admin_list_with_extra_buttons.html"

    def get_extra_buttons(self):
        # should return action as { title, path, method }
        raise NotImplemented

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [path(extra['path'], extra['method'])
                      for extra in self.get_extra_buttons()]
        return extra_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['extra_buttons'] = self.get_extra_buttons()
        return super().changelist_view(request, extra_context=extra_context)

    def trigger_task(self, request, task):
        result = task.delay()
        self.message_user(
            request,
            mark_safe("<a href='{}'>Tâche {} ajoutée à la file</a> ({})".format(
                reverse_lazy('admin:django_celery_results_taskresult_changelist'), result.task_id, result.status))
        )
        return HttpResponseRedirect("../")


class AiracUpdateMixin(ExtraButtonsMixin):

    def get_extra_buttons(self):
        buttons = [{
            'title': 'Mettre à jour AIP',
            'path': 'trigger-update/',
            'method': self.trigger_update
        }]
        if config.FALLBACK_URL:
            buttons.append({'title': 'Télécharger depuis Fallback',
                           'path': 'trigger-fallback/', 'method': self.trigger_fallback})
        return buttons

    def trigger_update(self, request):
        return self.trigger_task(request, download_last_airac)

    def trigger_fallback(self, request):
        return self.trigger_task(request, pull_from_diapason)


try:
    from app.version import __version__
    admin.site.site_header = mark_safe("Diapason eNews Admin <span style='font-size:0.8125rem;'>({})</span>".format(
        __version__))
except:
    admin.site.site_header = "Diapason eNews Admin"
