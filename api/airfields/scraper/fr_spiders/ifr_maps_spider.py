from .ad_generic_spider import GenericADSpider
from ..items import AirfieldMapItem
from scraper.spider_utils import make_root_url

# scrapy crawl ifr_maps -a airac=2021-03-25


# Airfield content page for a given airfield ICAO code (LFZZ)
URL_SELECTOR = 'a::attr(href)'
MAP_FILENAME_REGEX = r'Cartes.*.pdf'
MAP_FILTERS = sum([['_{}_'.format(f), ' {}'.format(f)]
                   for f in ['DATA', 'AOC', 'GMC', 'CODE', 'APDC',
                             'COM', 'TEXT', 'PATC']], [])


class IFRMapsSpider(GenericADSpider):
    name = "ifr_maps"

    def parse_ad_page(self, response, airac, airfield):
        # crawls airfield content page to get list of map files
        # then returns list of map items (see pipelines for additional
        # treatment)
        # FilePipeline automatically downloads any linked file to /media
        root_url = make_root_url(airac)
        for map_file in response.css(URL_SELECTOR).re(MAP_FILENAME_REGEX):
            if all(s not in map_file for s in MAP_FILTERS):
                map_name = self._get_map_name_from_filename(map_file, airfield)
                yield AirfieldMapItem(
                    airac=airac,
                    airfield=airfield,
                    name=map_name,
                    file_urls=["{}{}".format(root_url, map_file)]
                )

    def _get_map_name_from_filename(self, filename, airfield):
        # input: Cartes/LFLV/AD_2_LFLV_STAR_RWY_ALL_RNAV_INSTR_01.pdf
        # output : STAR_RWY_ALL_RNAV_INSTR_01
        return filename.split(airfield + " ")[-1]\
            .split(airfield + "_")[-1]\
            .split(".")[0]
