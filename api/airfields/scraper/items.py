import scrapy
from scrapy_djangoitem import DjangoItem

from ..models import AirfieldFrequency, AirfieldMap, Airfield


class AirfieldMapItem(DjangoItem):
    django_model = AirfieldMap
    file_urls = scrapy.Field()
    files = scrapy.Field()


class AirfieldItem(DjangoItem):
    django_model = Airfield
    airac = scrapy.Field()


class AirfieldFrequencyItem(DjangoItem):
    django_model = AirfieldFrequency
