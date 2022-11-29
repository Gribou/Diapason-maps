import scrapy
from scrapy_djangoitem import DjangoItem

from civ.models import AzbaSchedule, AzbaKnownSchedule, AzbaArea


class AzbaScheduleItem(DjangoItem):
    django_model = AzbaSchedule


class AzbaKnownScheduleItem(DjangoItem):
    django_model = AzbaKnownSchedule


class AzbaAreaItem(DjangoItem):
    django_model = AzbaArea
