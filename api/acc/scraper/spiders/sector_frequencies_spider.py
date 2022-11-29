import scrapy
import logging
import re

from scraper.spider_utils import (SIA_URL, get_airac_date_from_arg,
                                  make_root_url, extract_field_value_from_row)
from ..items import SectorFrequencyItem

logger = logging.getLogger('django')

UHF_FLOOR = 200

INDEX_URL = "FR-GEN-3.4-fr-FR.html#GEN-3.4"
DATA_SELECTOR = "table[class*=center-label]"
ROW_SELECTOR = "tr"
ROW_CENTER_NAME_SELECTOR = "span[id*=AIRSPACE\.TXT_NAME]"
ROW_CENTER_TYPE_SELECTOR = "span[id*=FREQUENCY\.CODE_TYPE--1]"
ROW_ACS_SELECTOR = "span[id*=FREQUENCY\.CODE_TYPE]"
ROW_SECTOR_NAME_SELECTOR = "span[id*=FREQUENCY\.SECTEUR_SITUATION]"
ROW_FREQ_SELECTOR = "span[id*=FREQUENCY\.VAL_FREQ_TRANS]"
ROW_FREQ_TYPE_SELECTOR = "span[id*=FREQUENCY\.UOM_FREQ]"
ROW_FREQ_RMK_SELECTOR = "span[id*=FREQUENCY\.TXT_RMK_NAT]"


# scrapy crawl sectors_frequency -a airac=2021-03-25


class SectorFrequencySpider(scrapy.Spider):
    name = "sectors_frequency"
    allowed_urls = [SIA_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = make_root_url(airac_date)
        yield scrapy.Request(url="{}{}".format(root_url, INDEX_URL),
                             callback=self.parse,
                             cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        failed_sectors = []
        center_name = ''
        sectors_names_raw = ''
        table = response.css(DATA_SELECTOR)
        for row in table.css(ROW_SELECTOR):
            # TRY to extract data from a line in the table
            try:
                # TRY TO GET Control Center Name -> Line
                new_center_name = extract_field_value_from_row(
                    row, ROW_CENTER_NAME_SELECTOR).get()
                new_center_type = extract_field_value_from_row(
                    row, ROW_CENTER_TYPE_SELECTOR).get()
                # If found then store value while another name is found
                if new_center_name and new_center_type:
                    center_name = '{} {}'.format(
                        new_center_name, new_center_type)
                # If no Control Center name found -> sector definition
                else:
                    # Collect sector data
                    frequency_raw = extract_field_value_from_row(
                        row, ROW_FREQ_SELECTOR).getall()
                    frequency = self.get_clean_frequency(frequency_raw)
                    sectors_names_raw = extract_field_value_from_row(
                        row, ROW_SECTOR_NAME_SELECTOR).getall()
                    sectors_type = extract_field_value_from_row(
                        row, ROW_ACS_SELECTOR).get()
                    # If sector name exists
                    if sectors_names_raw and self.check_sector_type(sectors_type):
                        sectors_names = self.extract_sectors_names(
                            sectors_names_raw)
                        freq = {'value': frequency,
                                'type': self.get_frequency_type(frequency)}
                        for sector_name in sectors_names:
                            yield SectorFrequencyItem(
                                name=sector_name,
                                control_center=center_name,
                                frequency=freq,
                                airac=airac
                            )
            except Exception as e:
                failed_sectors.append(str(sectors_names_raw))
                logger.error(e)
        if failed_sectors:
            logger.error("Parse errors for sectors : {}".format(
                ', '.join(failed_sectors)))

    def extract_sectors_names(self, name_list):
        '''Returns clean sector list of names'''
        return [n.strip() for name in name_list for n in re.split(r'[,/]', name.replace("\r\n", "")) if len(n.strip()) > 0]

    def check_sector_type(self, name):
        '''Returns if sector type is correct'''
        if name:
            return name in ['ACS', 'UAC']
        return False

    def get_clean_frequency(self, frequency_list):
        return ''.join([frequency.replace("\r\n", "").strip() for frequency in frequency_list])

    def get_frequency_type(self, frequency):
        '''Returns frequency type (VHF or UHF) according to its value'''
        freq_float = float(frequency)
        if freq_float > UHF_FLOOR:
            return 'U'
        return 'V'
