import scrapy
import os

from scraper.spider_utils import get_airac_date_from_arg
from ..items import AirfieldItem, AirfieldMapItem

# scrapy crawl nats_airfields -a airac=2022-04-21

NATS_URL = "www.aurora.nats.co.uk"
ROOT_URL_TEMPLATE = "https://www.aurora.nats.co.uk/htmlAIP/Publications/{}-AIRAC/html/eAIP/"
GRAPHICS_URL_TEMPLATE = "https://www.aurora.nats.co.uk/htmlAIP/Publications/{}-AIRAC/graphics/"

AD_INDEX_URL = "EG-AD-1.3-en-GB.html"
AD_ROW_SELECTOR = "tbody tr:not([id='ADSTAB'])"
AD_CODE_SELECTOR = "td:nth-child(2) .SD *::text"
AD_TYPES_SELECTOR = "td:nth-child(3) *::text"
AD_RULES_SELECTOR = "td:nth-child(4) *::text"
AD_SCHEDULED_SELECTOR = "td:nth-child(5) *::text"
AD_CODE_FILTERS = ["EGP", "EGA"]

AD_URL_TEMPLATE = "EG-AD-2.{}-en-GB.html"
AD_NAME_SELECTOR = "div[id$='2.1'] .ADName ::text"
GEO_DATA_ROW_SELECTOR = "div[id$='2.2'] td:last_child"
GEO_LAT_REGEX = r'[0-9]{6}[NS]'
GEO_LON_REGEX = r'[0-9]{7}[EW]'

MAP_TABLE_SELECTOR = "div[id$='2.24'] tr"
URL_SELECTOR = "a[href$='.pdf']::attr(href)"
MAP_CONTENT_SELECTOR = "td *::text"
MAP_FILTERS = ['GROUND MOVEMENT', 'PARKING', "VISUAL",
               'CODING', 'TEXT', 'HELICOPTER', 'LOCAL', 'DE-ICING']
MAP_ALIASES = [
    ('INSTRUMENT APPROACH CHART', 'IAC'),
    ('INITIAL APPROACH PROCEDURE', 'IAP'),
    ('INITIAL APPROACH PROCEDURES', 'IAP'),
    ('STANDARD INSTRUMENT ARRIVAL', 'STAR'),
    ('STANDARD ARRIVAL CHART - INSTRUMENT (STAR)', 'STAR'),
    ('STANDARD DEPARTURE CHART - INSTRUMENT (SID)', 'SID'),
    ('AERODROME CHART', 'ADC'),
    ('(DME/DME or GNSS) ', "")
]


class NATSAirfieldsSpider(scrapy.Spider):
    name = "nats_airfields"
    allowed_urls = [NATS_URL]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        root_url = ROOT_URL_TEMPLATE.format(airac_date.strftime("%Y-%m-%d"))
        yield scrapy.Request(url="{}{}".format(root_url, AD_INDEX_URL), callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        for row in response.css(AD_ROW_SELECTOR):
            if "INTL" in "".join(row.css(AD_TYPES_SELECTOR).extract()) and "IFR" in "".join(row.css(AD_RULES_SELECTOR).extract()) and "S" in "".join(row.css(AD_SCHEDULED_SELECTOR).extract()):
                icao_code = row.css(AD_CODE_SELECTOR).get()
                if icao_code[:3] not in AD_CODE_FILTERS:
                    yield response.follow(AD_URL_TEMPLATE.format(icao_code),
                                          callback=self.parse_ad_page, cb_kwargs={'airac': airac, 'icao_code': icao_code})

    def parse_ad_page(self, response, airac, icao_code):
        name = response.css(AD_NAME_SELECTOR).get().replace(
            "\n", "").split('—')[1].strip()
        elevation = response.css(
            GEO_DATA_ROW_SELECTOR)[2].css("*::text").extract()[2]
        lat = self.format_latitude(response.css(
            GEO_DATA_ROW_SELECTOR).re(GEO_LAT_REGEX)[0])
        lon = self.format_longitude(response.css(
            GEO_DATA_ROW_SELECTOR).re(GEO_LON_REGEX)[0])
        if int(lat[0:2]) <= 52:
            yield AirfieldItem(icao_code=icao_code, name=name, latitude=lat, longitude=lon, elevation=[elevation], airac=airac, category="public aerodrome")
            graphics_url = GRAPHICS_URL_TEMPLATE.format(
                airac.strftime("%Y-%m-%d"))
            filetitle = None
            for row in response.css(MAP_TABLE_SELECTOR):
                url = row.css(URL_SELECTOR).extract()
                if url:
                    fileurl = "{}{}".format(
                        graphics_url, os.path.basename(url[0]))
                    if filetitle is not None:
                        yield AirfieldMapItem(airac=airac, airfield=icao_code, name=filetitle, file_urls=[fileurl])
                    filetitle = None
                else:
                    filetitle = self.format_filetitle(row)

    def format_latitude(self, latitude):
        return latitude[:2] + "°" + latitude[2:4] + "'" + latitude[4:6] + '"' + latitude[-1]

    def format_longitude(self, longitude):
        return longitude[:3] + "°" + longitude[3:5] + "'" + longitude[5:7] + '"' + longitude[-1]

    def format_filetitle(self, row):
        filetitle = row.css(MAP_CONTENT_SELECTOR).extract()[1]
        if not all(s not in filetitle for s in MAP_FILTERS):
            return None
        for name, alias in MAP_ALIASES:
            filetitle = filetitle.replace(name, alias)
        return filetitle.replace(" - ICAO", "")
