

# fetch missing areas only ?
# update all existing areas ?

import scrapy
import logging

from scraper.spider_utils import (
    SIA_URL, get_airac_date_from_arg, make_root_url, extract_field_value_from_row)
from ..items import AzbaAreaItem

logger = logging.getLogger("django")

INDEX_URL = "FR-ENR-5.1-fr-FR.html#ENR-5.1-1"
AREA_ROW_SELECTOR = "tr[id*=TXT_NAME],tr[id*=VER_UPPER]"
NAME_TEXT_SELECTOR = "td:first-child span[id*='TXT_NAME']::text,span:not([id])::text"
CEILING_SELECTOR = "span[id*=VER_UPPER]"
FLOOR_SELECTOR = "span[id*=VER_LOWER]"
ROW_BOUNDARY_SELECTOR = "span[id*=GEO_LAT], span[id*=GEO_LONG], span[id*=GEO_BORDER], span[id*=ARC]"
LATITUDE_ID_SELECTOR = "GEO_LAT"
LONGITUDE_ID_SELECTOR = "GEO_LON"
BORDER_ID_SELECTOR = "GEO_BORDER"
ARC_ID_SELECTOR = "ARC"
GEO_REGEX = r'.{9,10}[EWNS]'

IGNORED_AREAS = []


# scrapy crawl azba_boundaries -a airac=2022-04-21

class AzbaBoundariesSpider(scrapy.Spider):
    name = "azba_boundaries"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(root_url, INDEX_URL),
                             callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        rows = response.css(AREA_ROW_SELECTOR)
        area_name = None
        for i, row in enumerate(rows):
            name_extract = row.css(NAME_TEXT_SELECTOR).getall()
            if name_extract:
                area_name = [r.replace("Z", "Z").strip()
                             for r in row.css(NAME_TEXT_SELECTOR).getall()]
            # this Z is a special character that does not show everywhere
                area_name = "".join([r for r in area_name if r and r != "LF"])
            elif area_name and area_name not in IGNORED_AREAS:
                # this is a the data row for current area_name
                ceiling = extract_field_value_from_row(
                    row, CEILING_SELECTOR).get()
                floor = extract_field_value_from_row(row, FLOOR_SELECTOR).get()
                boundaries = self.parse_boundaries(row)
                if boundaries:
                    yield AzbaAreaItem(label=area_name, ceiling=ceiling, floor=floor, airac=airac, boundaries=boundaries)

    def parse_boundaries(self, row):
        boundaries = []
        current_latitude = None
        for item in row.css(ROW_BOUNDARY_SELECTOR):
            id = item.css("*::attr(id)").get()
            content = item.css("*::text")
            if ARC_ID_SELECTOR in id:
                # FIXME this is an arc portion, unable to parse for now
                pass
            elif BORDER_ID_SELECTOR in id:
                boundaries.append([content.get()])
            elif LATITUDE_ID_SELECTOR in id:
                current_latitude = content.re(GEO_REGEX)[0]
            elif LONGITUDE_ID_SELECTOR in id:
                boundaries.append([current_latitude, content.re(GEO_REGEX)[0]])
                current_latitude = None
        return boundaries
