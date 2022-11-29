import scrapy

from scraper.spider_utils import (
    SIA_URL, get_airac_date_from_arg, make_root_url, extract_field_value_from_row)
from ..items import RadioNavStationItem

INDEX_URL = "FR-ENR-4.1-fr-FR.html#ENR-4.1"
DATA_SELECTOR = "table.ENR-table tbody"
ROW_SELECTOR = "tr"
ROW_LONG_NAME_SELECTOR = "td:first-child span"
ROW_SHORT_NAME_SELECTOR = "span[id*=CODE_NAV_ID]"
ROW_TYPE_SELECTOR = "td:nth-child(2) span"
ROW_FREQUENCY_SELECTOR = "td:nth-child(4) span"
ROW_LAT_SELECTOR = "span[id*=GEO_LAT]"
ROW_LON_SELECTOR = "span[id*=GEO_LONG]"
ROW_RANGE_SELECTOR = "span[id*=PORTEE]"

GEO_REGEX = r'.{11,12}[EWNS]'

# scrapy crawl radionav -a airac=2021-03-25


class RadionavSpider(scrapy.Spider):
    name = "radionav"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(root_url, INDEX_URL),
                             callback=self.parse,
                             cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        table = response.css(DATA_SELECTOR)
        for row in table.css(ROW_SELECTOR):
            short_name = extract_field_value_from_row(
                row, ROW_SHORT_NAME_SELECTOR).get()
            if short_name is not None:
                yield RadioNavStationItem(
                    short_name=short_name,
                    long_name=extract_field_value_from_row(
                        row, ROW_LONG_NAME_SELECTOR).get(),
                    types=extract_field_value_from_row(
                        row, ROW_TYPE_SELECTOR).get(),
                    latitude=extract_field_value_from_row(
                        row, ROW_LAT_SELECTOR).re(GEO_REGEX)[0],
                    longitude=extract_field_value_from_row(
                        row, ROW_LON_SELECTOR).re(GEO_REGEX)[0],
                    frequency=' '.join(extract_field_value_from_row(
                        row, ROW_FREQUENCY_SELECTOR).extract()),
                    range=extract_field_value_from_row(
                        row, ROW_RANGE_SELECTOR).get(),
                    airac=airac
                )
