import scrapy
import logging

from scraper.spider_utils import (SIA_URL, get_airac_date_from_arg,
                                  make_root_url, get_pretty_airac_date, extract_field_value_from_row)
from ..items import AirfieldMapItem

logger = logging.getLogger('django')

INDEX_URL = "FR-AD-1.3-fr-FR.html"
ROW_SELECTOR = "tr[id*='ICAO']"
ROW_ICAO_CODE_SELECTOR = "span[id*=CODE_ICAO]"

NO_VAC_AIRFIELD_LIST = ['LFOA', 'LFOE', 'LFBC', 'LFBM', 'LFXQ', 'LFPC',
                        'LFKK', 'LFSX', 'LFSI', 'LFKS', 'LFSO', 'LFPR', 'LFMO', 'LFPV']
WITH_VACH_AIRFIELD_LIST = ['LFBD', 'LFBO', 'LFBP', 'LFBZ', 'LFLJ', 'LFLY',
                           'LFMD', 'LFML', 'LFMN', 'LFMT', 'LFPB', 'LFPG',
                           'LFPI', 'LFPN', 'LFPO', 'LFPZ', 'LFRS', 'LFSB']
MISSING_AIRFIELD_LIST = ['LFPI']

VAC_MAP_URL_TEMPLATE = "https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_{}/Atlas-VAC/PDF_AIPparSSection/VAC/AD/AD-2.{}.pdf"
VACH_MAP_URL_TEMPLATE = "https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_{}/Atlas-VAC/PDF_AIPparSSection/VACH/AD/AD-3.{}.pdf"


# scrapy crawl vfr_maps -a airac=2021-03-25

# There is no easily parsable index of VAC/VACH map files
# So we guess their urls from the airfield list in AD1.3

class VFRMapsSpider(scrapy.Spider):
    name = "vfr_maps"
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
            if icao_code and icao_code.startswith("LF") and icao_code not in NO_VAC_AIRFIELD_LIST:
                with_vach = icao_code in WITH_VACH_AIRFIELD_LIST
                pretty_airac_date = get_pretty_airac_date(airac)
                yield AirfieldMapItem(
                    airac=airac, airfield=icao_code, name="VAC", file_urls=[VAC_MAP_URL_TEMPLATE.format(pretty_airac_date, icao_code)])
                if with_vach:
                    yield AirfieldMapItem(
                        airac=airac, airfield=icao_code, name="VACH", file_urls=[VACH_MAP_URL_TEMPLATE.format(pretty_airac_date, icao_code)])
        logger.error("Parse errors for airfields : {}".format(
            ', '.join(failed_airfields)))
        for a in MISSING_AIRFIELD_LIST:
            yield from self.parse_vac_maps(airac, a)

    def parse_vac_maps(self, airac, icao_code):
        no_vac = not icao_code or icao_code in NO_VAC_AIRFIELD_LIST
        with_vach = icao_code in WITH_VACH_AIRFIELD_LIST
        pretty_airac_date = get_pretty_airac_date(airac)
        if not no_vac:
            yield AirfieldMapItem(airac=airac, airfield=icao_code, name="VAC", file_urls=[VAC_MAP_URL_TEMPLATE.format(pretty_airac_date, icao_code)])
            if with_vach:
                yield AirfieldMapItem(airac=airac, airfield=icao_code, name="VACH", file_urls=[VACH_MAP_URL_TEMPLATE.format(pretty_airac_date, icao_code)])
