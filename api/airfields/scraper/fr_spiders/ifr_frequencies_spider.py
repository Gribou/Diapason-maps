from .ad_generic_spider import GenericADSpider
from ..items import AirfieldFrequencyItem
from scraper.spider_utils import extract_field_value_from_row

# scrapy crawl ifr_frequencies -a airac=2021-03-25


FREQUENCY_ROW_SELECTOR = "tr[id*=VAL_FREQ_TRANS]"
FREQUENCY_ROW_TYPE_SELECTOR = "span[id*=SERVICE\.CODE_TYPE]"
FREQUENCY_ROW_VALUE_SELECTOR = "span[id*=FREQUENCY\.VAL_FREQ_TRANS]"
FREQUENCY_ROW_OBS_SELECTOR = "span[id*=FREQUENCY\.TXT_RMK_NAT]"

FREQUENCY_REGEX = r'[0-9]{3}\.[0-9]{3}'


class IFRFrequenciesSpider(GenericADSpider):
    name = "ifr_frequencies"

    def parse_ad_page(self, response, airac, airfield):
        for row in response.css(FREQUENCY_ROW_SELECTOR):
            yield AirfieldFrequencyItem(
                airfield=airfield,
                airac=airac,
                value=extract_field_value_from_row(
                    row, FREQUENCY_ROW_VALUE_SELECTOR).re(FREQUENCY_REGEX)[0],
                frequency_type=extract_field_value_from_row(
                    row, FREQUENCY_ROW_TYPE_SELECTOR).get(),
                comments=extract_field_value_from_row(
                    row, FREQUENCY_ROW_OBS_SELECTOR).get()
            )
