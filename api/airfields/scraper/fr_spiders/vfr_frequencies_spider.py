import scrapy
import re
import logging

from scraper.spider_utils import (SIA_URL, get_airac_date_from_arg,
                                  make_root_url, extract_field_value_from_row)
from ..items import AirfieldFrequencyItem

logger = logging.getLogger('django')

INDEX_URL = "FR-AD-1.6-fr-FR.html"
DATA_SELECTOR = "tr"
ROW_ICAO_CODE_SELECTOR = "span[id*=CODE_ICAO]"
ROW_NAME_SELECTOR = "span[id*=TXT_CALL_SIGN]"
ROW_FREQ_SELECTOR = "span[id*=VAL_FREQ_TRANS]"
ROW_FREQ_TYPE_SELECTOR = "span[id*=CODE_TYPE]"
ROW_FREQ_OBS_SELECTOR = "span[id*=TXT_RMK_NAT]"

# scrapy crawl frequency_airfields -a airac=2021-03-25


class VFRFrequenciesSpider(scrapy.Spider):
    name = "vfr_frequencies"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(root_url, INDEX_URL),
                             callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        # extract airfield frequencies from AD1.6
        failed_airfields = []
        old_icao = ''
        for row in response.css(DATA_SELECTOR):
            try:
                icao_code = extract_field_value_from_row(
                    row, ROW_ICAO_CODE_SELECTOR).get()
                if icao_code:
                    old_icao = icao_code
                else:
                    call_sign = extract_field_value_from_row(
                        row, ROW_NAME_SELECTOR).get()
                    freq = extract_field_value_from_row(
                        row, ROW_FREQ_SELECTOR).get()
                    freq_type_raw = extract_field_value_from_row(
                        row, ROW_FREQ_TYPE_SELECTOR).get()
                    freq_type = self.extract_frequency_type(
                        freq_type_raw, call_sign)
                    comments = extract_field_value_from_row(
                        row, ROW_FREQ_OBS_SELECTOR).get()
                    yield AirfieldFrequencyItem(
                        airfield=old_icao,
                        value=freq,
                        frequency_type=freq_type,
                        airac=airac,
                        comments=comments
                    )
            except:
                failed_airfields.append(old_icao)
        logger.error("Parse errors for airfields : {}".format(
            ', '.join(failed_airfields)))

    def extract_frequency_type(self, frequency_name, call_sign):
        if frequency_name == 'TWR' and re.search(r'Sol', call_sign):
            return 'GND'
        elif frequency_name == 'TWR' and re.search(r'Tour', call_sign):
            return 'TWR'
        else:
            return frequency_name
