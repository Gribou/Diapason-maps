import scrapy

from scraper.spider_utils import get_airac_date_from_arg
from ..items import RadioNavStationItem

# scrapy crawl nats_radionav -a airac=2022-07-14

NATS_URL = "www.aurora.nats.co.uk"
ROOT_URL_TEMPLATE = "https://www.aurora.nats.co.uk/htmlAIP/Publications/{}-AIRAC/html/eAIP/"

RADIONAV_URL = "EG-ENR-4.1-en-GB.html"
ROW_SELECTOR = "tbody tr[id*=NAV]"
ROW_LONG_NAME_SELECTOR = "td:first-child strong span::text"
ROW_TYPES_SELECTOR = "td:first-child p ::text"
ROW_SHORT_NAME_SELECTOR = "td:nth-child(2) span::text"
ROW_FREQUENCY_SELECTOR = "td:nth-child(3) span[class=SD]::text"
ROW_LAT_SELECTOR = "td:nth-child(5) span::text"
ROW_LON_SELECTOR = "td:nth-child(5) span::text"

GEO_LAT_REGEX = r'[0-9]{6}\.[0-9]{2}[NS]'
GEO_LON_REGEX = r'[0-9]{7}\.[0-9]{2}[EW]'


class NatsRadionavSpider(scrapy.Spider):
    name = "nats_radionav"
    allowed_urls = [NATS_URL]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = ROOT_URL_TEMPLATE.format(airac_date.strftime("%Y-%m-%d"))
        yield scrapy.Request(url="{}{}".format(root_url, RADIONAV_URL), callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        for row in response.css(ROW_SELECTOR):
            short_name = row.css(ROW_SHORT_NAME_SELECTOR).get()
            latitude = self.format_latitude(
                row.css(ROW_LAT_SELECTOR).re(GEO_LAT_REGEX)[0])
            if short_name is not None and int(latitude[0:2]) <= 52:
                yield RadioNavStationItem(
                    short_name=short_name,
                    long_name=row.css(ROW_LONG_NAME_SELECTOR).get(),
                    types=self.format_types(
                        row.css(ROW_TYPES_SELECTOR).extract()),
                    latitude=latitude,
                    longitude=self.format_longitude(
                        row.css(ROW_LON_SELECTOR).re(GEO_LON_REGEX)[0]),
                    frequency=" ".join(
                        row.css(ROW_FREQUENCY_SELECTOR).extract()),
                    airac=airac)

    def format_types(self, data):
        result = []
        for s in data:
            if all([c not in s for c in ["\n", "°", ";", ")", "(", "20"]]):
                result.append(s.replace("/", "").strip())
        return "-".join(result)

    def format_latitude(self, latitude):
        return latitude[:2] + "°" + latitude[2:4] + "'" + latitude[4:6] + '"' + latitude[-1]

    def format_longitude(self, longitude):
        return longitude[:3] + "°" + longitude[3:5] + "'" + longitude[5:7] + '"' + longitude[-1]
