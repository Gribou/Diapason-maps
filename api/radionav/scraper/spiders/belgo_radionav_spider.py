import scrapy

from scraper.spider_utils import get_airac_date_from_arg
from ..items import RadioNavStationItem

# scrapy crawl belgo_radionav -a airac=2022-04-21

SKEYES_URL = "ops.skeyes.be"
ROOT_URL = "https://ops.skeyes.be/html/belgocontrol_static/eaip/eAIP_Main/html/eAIP/EB-ENR-4.1-en-GB.html"
ROW_SELECTOR = "tbody tr[id*=SP]"
ROW_LONG_NAME_SELECTOR = "td:first-child::text"
ROW_TYPES_SELECTOR = "td:first-child acronym::text"
ROW_SHORT_NAME_SELECTOR = "td:nth-child(2) *::text"
ROW_FREQUENCY_SELECTOR = "td:nth-child(3) *::text"
ROW_LAT_SELECTOR = "td:nth-child(5) p::text"
ROW_LON_SELECTOR = "td:nth-child(5) p::text"
ROW_RANGE_SELECTOR = "td:last-child *::text"

GEO_LAT_REGEX = r'[0-9]{6}[NS]'
GEO_LON_REGEX = r'[0-9]{7}[EW]'


class BelgoRadionavSpider(scrapy.Spider):
    name = "belgo_radionav"
    allowed_urls = [SKEYES_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        yield scrapy.Request(url=ROOT_URL, callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        for row in response.css(ROW_SELECTOR):
            short_name = row.css(ROW_SHORT_NAME_SELECTOR).get()
            types = "-".join(row.css(ROW_TYPES_SELECTOR).extract())
            if short_name is not None and "TACAN" not in types:
                yield RadioNavStationItem(
                    short_name=short_name,
                    long_name=row.css(ROW_LONG_NAME_SELECTOR).get(),
                    types=types,
                    frequency=self.format_frequency(
                        row.css(ROW_FREQUENCY_SELECTOR).extract()),
                    latitude=self.format_latitude(
                        row.css(ROW_LAT_SELECTOR).re(GEO_LAT_REGEX)[0]),

                    longitude=self.format_longitude(
                        row.css(ROW_LON_SELECTOR).re(GEO_LON_REGEX)[0]
                    ),
                    range=self.format_range(
                        row.css(ROW_RANGE_SELECTOR).extract()),
                    airac=airac)

    def format_frequency(self, frequency):
        return "".join(frequency).replace("\u2009", " ") \
            .replace("(", " (").replace(")", ") ")

    def format_range(self, range):
        return "".join(range).split("OPR:")[0].split("FRA")[0].replace("\u2009", " ").replace("0DOC", "0 - ").replace("DOC: ", "")

    def format_latitude(self, latitude):
        return latitude[:2] + "°" + latitude[2:4] + "'" + latitude[4:6] + '"' + latitude[-1]

    def format_longitude(self, longitude):
        return longitude[:3] + "°" + longitude[3:5] + "'" + longitude[5:7] + '"' + longitude[-1]
