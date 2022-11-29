from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms

from api.admin import ExtraButtonsMixin
from .models import TelephoneCategory, Telephone
from .tasks import import_csv_phonebook


@admin.register(TelephoneCategory)
class TelephoneCategoryAdmin(admin.ModelAdmin):
    model = TelephoneCategory
    list_display = ['name', 'rank']
    search_fields = ['name']
    ordering = ['rank', 'name']


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label='Fichier CSV')


@admin.register(Telephone)
class TelephoneAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    model = Telephone
    list_display = ['name', 'category', 'telephone_number',
                    'isExterior', 'isCDS', 'isW', 'isE', 'alias', 'update_date']
    ordering = ['category', 'telephone_number', 'name']
    search_fields = ['category__name', 'name', 'telephone_number', 'alias']

    def get_extra_buttons(self):
        return [{
            'title': 'Charger de nouvelles données',
            'path': 'import-csv/',
            'method': self.import_csv
        }]

    def import_csv(self, request):
        """Imports data from CSV file into Telephone table"""
        if request.method == "POST" and request.FILES:
            uploaded_file = request.FILES['csv_file']
            file_name = default_storage.save(uploaded_file.name, uploaded_file)
            result = import_csv_phonebook.delay(file_name)
            self.message_user(
                request,
                mark_safe("<a href='{}'>Tâche {} ajoutée à la file</a> ({})".format(reverse_lazy(
                    'admin:django_celery_results_taskresult_changelist'), result.task_id, result.status))
            )
            return HttpResponseRedirect("../")
        return render(
            request, "phones/admin/csv_form.html", {"form": CsvImportForm()}
        )
