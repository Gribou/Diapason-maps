import scrapy

from scrapy_djangoitem import DjangoItem

from ..models import RadioNavStation


class RadioNavStationItem(DjangoItem):
    django_model = RadioNavStation
    types = scrapy.Field()
    airac = scrapy.Field()
