import scrapy
import logging

from scraper.spider_utils import (SIA_URL, get_airac_date_from_arg,
                    make_root_url, extract_field_value_from_row)
from ..items import AirfieldItem

logger = logging.getLogger('django')

INDEX_URL = "FR-AD-1.3-fr-FR.html"
ROW_SELECTOR = "tr[id*='ICAO']"
ROW_ICAO_CODE_SELECTOR = "span[id*=CODE_ICAO]"
ROW_NAME_SELECTOR = "span[id*=TXT_NAME]"
ROW_LAT_SELECTOR = "span[id*=GEO_LAT]"
ROW_LON_SELECTOR = "span[id*=GEO_LONG]"
ROW_ELEV_SELECTOR = "span[id*=VAL_ELEV]"
ROW_STATUS_SELECTOR = "span[id*=STATUT]"

GEO_REGEX = r'.{9,10}[EWNS]'

MISSING_AIRFIELD_LIST = [
    {'icao_code': 'LFPI', 'name': 'PARIS ISSY LES MOULINEAUX', 'category':
     'hélistation', 'latitude': '48°50\'00"N', 'longitude': '002°16\'22"E',
     'elevation': ['165']}]

# scrapy crawl airfields -a airac=2021-03-25


class AirfieldsSpider(scrapy.Spider):
    name = "airfields"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        self.root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(self.root_url, INDEX_URL),
                             callback=self.parse,
                             cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        # extract airfields from AD1.3.1 and download VAC and VACH maps
        failed_airfields = []
        for row in response.css(ROW_SELECTOR):
            icao_code = extract_field_value_from_row(
                row, ROW_ICAO_CODE_SELECTOR).get()
            # !! do not parse helistations
            if icao_code and icao_code.startswith("LF"):
                try:
                    yield from self.parse_airfield(row, airac, icao_code)
                except:
                    failed_airfields.append(icao_code)
        logger.error("Parse errors for airfields : {}".format(
            ', '.join(failed_airfields)))
        for a in MISSING_AIRFIELD_LIST:
            yield AirfieldItem(airac=airac, **a)

    def parse_airfield(self, row, airac, icao_code):
        yield AirfieldItem(
            icao_code=icao_code,
            name=extract_field_value_from_row(
                row, ROW_NAME_SELECTOR).get(),
            latitude=extract_field_value_from_row(
                row, ROW_LAT_SELECTOR).re(GEO_REGEX)[0],
            longitude=extract_field_value_from_row(
                row, ROW_LON_SELECTOR).re(GEO_REGEX)[0],
            elevation=extract_field_value_from_row(
                row, ROW_ELEV_SELECTOR).re(r'[0-9]+'),
            category=extract_field_value_from_row(
                row, ROW_STATUS_SELECTOR).get(),
            airac=airac,
        )
