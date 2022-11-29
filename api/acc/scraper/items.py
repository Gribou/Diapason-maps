import scrapy
from scrapy_djangoitem import DjangoItem

from ..models import Sector, SectorPart


class SectorFrequencyItem(DjangoItem):
    django_model = Sector
    frequency = scrapy.Field()
    airac = scrapy.Field()


class SectorPartItem(DjangoItem):
    django_model = SectorPart
    sector_name = scrapy.Field()
    airac = scrapy.Field()
    boundaries = scrapy.Field()
