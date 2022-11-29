import scrapy
import re
import os

from scraper.spider_utils import get_airac_date_from_arg
from ..items import AirfieldItem, AirfieldMapItem

# scrapy crawl belgo_airfields -a airac=2022-04-21

SKEYES_URL = "ops.skeyes.be"
ROOT_URL = "https://ops.skeyes.be/html/belgocontrol_static/eaip/eAIP_Main/html/eAIP/"
GRAPHICS_URL = "https://ops.skeyes.be/html/belgocontrol_static/eaip/eAIP_Main/graphics/eAIP/"
# as the list of public aerodroms is limited, it is more efficient to hard-code here than to scrape EB-AD-1.3-en-GB.html and filter by type of airfields
AIRFIELD_LIST = ['EBAW', 'EBBR', 'EBCI', 'EBKT', 'EBLG', 'ELLX', 'EBOS']
AIRFIELD_URL_TEMPLATE = "EB-AD-2.{}-en-GB.html"

NAME_SELECTOR = "p[class=ADName]::text"
DATA_TABLE_TEXT_SELECTOR = "div[id$='2.2'] td:last-child"
COORDINATES_REGEX = r'([0-9]{6}N) ([0-9]{7}E)'
ELEVATION_REGEX = r'^([0-9\s]+).?FT / [0-9]+°C'

MAP_TABLE_SELECTOR = "div[id$='2.24'] tr"
URL_SELECTOR = "a[href$='.pdf']::attr(href)"
MAP_TITLE_SELECTOR = "td:first_child ::text"
MAP_SUBTITLE_SELECTOR = "td:last_child ::text"
MAP_FILTERS = ['GMC', 'APDC', 'AOC', 'PATC']
MAP_SUBTITLE_FILTERS = ["Datablock"]


class BelgoAirfieldsSpider(scrapy.Spider):
    name = "belgo_airfields"
    allowed_urls = [SKEYES_URL]

    def start_requests(self):
        airac_date = get_airac_date_from_arg(self)
        for icao_code in AIRFIELD_LIST:
            url = "{}{}".format(
                ROOT_URL, AIRFIELD_URL_TEMPLATE.format(icao_code))
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'airac': airac_date, 'icao_code': icao_code})

    def parse(self, response, airac, icao_code):
        name = response.css(NAME_SELECTOR).get().split('—')[1].strip()
        coordinates = []
        elevation = None
        for row in response.css(DATA_TABLE_TEXT_SELECTOR):
            coordinates = row.re(COORDINATES_REGEX)
            if coordinates:
                latitude = self.format_latitude(coordinates[0])
                longitude = self.format_longitude(coordinates[1])
            row_text = "".join(row.css("::text").extract())
            elevation_re = re.search(ELEVATION_REGEX, row_text)
            if elevation_re:
                elevation = elevation_re.group(1).replace(
                    " ", "").replace(u"\u2009", "")
        yield AirfieldItem(icao_code=icao_code, name=name, latitude=latitude, longitude=longitude, elevation=[elevation], airac=airac, category="public aerodrome")
        filetitle = None
        for row in response.css(MAP_TABLE_SELECTOR):
            url = row.css(URL_SELECTOR).extract()
            if url:
                fileurl = "{}{}".format(GRAPHICS_URL, os.path.basename(url[0]))
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
        filetitle = row.css(MAP_TITLE_SELECTOR).get().split('-')[1]
        if not all(s not in filetitle for s in MAP_FILTERS):
            return None
        filesubtitle = row.css(MAP_SUBTITLE_SELECTOR).get()
        if not all(s not in filesubtitle for s in MAP_SUBTITLE_FILTERS):
            return None
        filesubtitle = filesubtitle.split(
            ":")[-1].strip() if ":" in filesubtitle else None
        filetitle = "{} - {}".format(filetitle,
                                     filesubtitle) if filesubtitle else filetitle
        return filetitle
