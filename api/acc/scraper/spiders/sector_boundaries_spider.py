import scrapy
import re
import logging

from scraper.spider_utils import (
    SIA_URL, get_airac_date_from_arg, make_root_url, extract_field_value_from_row)
from ..items import SectorPartItem

from ...models import SectorPart

logger = logging.getLogger("django")

INDEX_URL = "FR-ENR-2.2-fr-FR.html#ENR-2.2"
ROW_SELECTOR = "tr[id*=UOM_DIST_VER_UPPER]"
ROW_NAME_SELECTOR = "span[id*=TXT_NAME]"
ROW_CEILING_SELECTOR = "span[id*=VER_UPPER]"
ROW_FLOOR_SELECTOR = "span[id*=VER_LOWER]"
ROW_BOUNDARY_SELECTOR = "span[id*=GEO_LAT], span[id*=GEO_LONG], span[id*=GEO_BORDER]"
LATITUDE_ID_SELECTOR = "GEO_LAT"
LONGITUDE_ID_SELECTOR = "GEO_LON"
BORDER_ID_SELECTOR = "GEO_BORDER"
GEO_REGEX = r'.{9,10}[EWNS]'

SECTOR_ALIASES = {
    "H1": "BN", "H2": "BN", "H3": "BN", "H4": "BN", "H5": "BN",
    "B1": "B3", "B2": "B3", "E3": "E2", "F1": "F3", "F2": "F3", "F4": "F3",
    "M1": "M4", "M2": "M4", "M3": "M4"
}

# TODO how to get arcs ? (ex : LE1)


# scrapy crawl sectors_boundaries -a airac=2022-04-21


class SectorBoundariesSpider(scrapy.Spider):
    name = "sectors_boundaries"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(root_url, INDEX_URL), callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        for row in response.css(ROW_SELECTOR):
            yield SectorPartItem(
                sector_name=extract_field_value_from_row(
                    row, ROW_NAME_SELECTOR).get(),
                floor=extract_field_value_from_row(
                    row, ROW_FLOOR_SELECTOR).get(),
                ceiling=extract_field_value_from_row(
                    row, ROW_CEILING_SELECTOR).get(),
                boundaries=self.parse_boundaries(row),
                airac=airac
            )

    def parse_boundaries(self, row):
        boundaries = []
        current_latitude = None
        for item in row.css(ROW_BOUNDARY_SELECTOR):
            id = item.css("*::attr(id)").get()
            content = item.css("*::text")
            if BORDER_ID_SELECTOR in id:
                boundaries.append([content.get()])
            elif LATITUDE_ID_SELECTOR in id:
                current_latitude = content.re(GEO_REGEX)[0]
            elif LONGITUDE_ID_SELECTOR in id:
                boundaries.append([current_latitude, content.re(GEO_REGEX)[0]])
                current_latitude = None
        return boundaries


def post_process():
    # Some sector boundaries are not declared explicitly in AIP
    # Because they are the same as the sector above or below
    # So we populate boundaries for these sectors from the ones of aliases
    for part in SectorPart.objects.filter(boundaries__isnull=True).all():
        alias_part = SectorPart.objects.filter(
            sector__name=SECTOR_ALIASES.get(part.sector.name, None)).first()
        part.boundaries = alias_part.boundaries
        part.save()
