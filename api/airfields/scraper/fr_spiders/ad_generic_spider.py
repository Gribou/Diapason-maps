import scrapy
import re

from scraper.spider_utils import SIA_URL, make_root_url, get_airac_date_from_arg


# Table of content page
INDEX_URL = "FR-menu-fr-FR.html"
# CSS selector for airfield list (has duplicates) from table of content page
AIRFIELD_URL_SELECTOR = "#ADdetails a::attr(href)"
AIRFIELD_URL_REGEX = r'.*LF[A-Z]{2}.*html'
AIRFIELD_NAME_REGEX = r"LF[A-Z]{2}"

# Airfield content page for a given airfield ICAO code (LFZZ)
URL_SELECTOR = 'a::attr(href)'


class GenericADSpider(scrapy.Spider):
    allowed_domains = [SIA_URL]

    def start_requests(self):
        # fetches eAIP table of content for a given AIRAC cycle
        # gets requested AIRAC cycle date from argument 'airac'
        # (ex : 2021-04-22)
        airac_date = get_airac_date_from_arg(self)
        yield scrapy.Request(
            url="{}{}".format(make_root_url(airac_date), INDEX_URL),
            callback=self.parse, cb_kwargs={'airac': airac_date})

    def parse(self, response, airac):
        # crawls eAIP AD2 table of content to get an airfield page list
        # then fetches eAIP page for each airfield
        airfield_pages = response.css(
            AIRFIELD_URL_SELECTOR).re(AIRFIELD_URL_REGEX)
        # remove duplicates and sort
        airfield_pages = list(dict.fromkeys(airfield_pages))
        airfield_pages.sort()
        for page in airfield_pages:
            airfield_name = re.search(AIRFIELD_NAME_REGEX, page).group()
            yield response.follow(
                page,
                callback=self.parse_ad_page,
                cb_kwargs={'airac': airac, 'airfield': airfield_name})

    def parse_ad_page(self, response, airac, airfield):
        raise NotImplementedError

