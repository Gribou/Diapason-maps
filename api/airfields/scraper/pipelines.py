
from scraper.clean import clean_pdf, clean_latitude, clean_longitude
from ..models import AirfieldMap, Airfield, AirfieldFrequency, FREQUENCY_TYPE
from .items import AirfieldItem, AirfieldMapItem, AirfieldFrequencyItem
from .clean import clean_category, clean_elevation, clean_map_name


class AirfieldPipeline:

    def process_item(self, item, spider):
        # creates a Django object for any scraped item and saves it to db
        if isinstance(item, AirfieldItem):
            self._process_airfield(item)
        return item

    def _process_airfield(self, item):
        if item['icao_code']:
            Airfield.objects.update_or_create(
                icao_code=item['icao_code'], defaults={
                    'name': item['name'],
                    'latitude': clean_latitude(item['latitude']),
                    'longitude': clean_longitude(item['longitude']),
                    'elevation': clean_elevation(item['elevation']),
                    'category': clean_category(item['category'])
                })
        return item


class MapPipeline:

    def process_item(self, item, spider):
        # creates a Django object for any scraped item and saves it to db
        if isinstance(item, AirfieldMapItem):
            self._process_map(item)
        return item

    def _process_map(self, item):
        if item['airfield']:
            airfield, _ = Airfield.objects.get_or_create(
                icao_code=item['airfield'])
            file = clean_pdf(item['files'])
            if file:
                AirfieldMap.objects.update_or_create(
                    airfield=airfield, name=clean_map_name(item['name']),
                    defaults={'airac': item['airac'], 'pdf': file})


class AirfieldFrequencyPipeline:

    def process_item(self, item, spider):
        if isinstance(item, AirfieldFrequencyItem):
            self._process_airfield_frequency(item)
        return item

    def _process_airfield_frequency(self, item):
        if item['airfield']:
            airfield, _ = Airfield.objects.get_or_create(
                icao_code=item['airfield'])
            freq_type = item['frequency_type']
            if self.validate_frequency_type(freq_type):
                # NOTE : an airfield may have multiple frequencies of each type
                AirfieldFrequency.objects.get_or_create(
                    airfield=airfield, frequency_type=freq_type,
                    value=item['value'], airac=item['airac'], comments=item['comments'])

    def validate_frequency_type(self, value):
        choices = FREQUENCY_TYPE
        for elt in choices:
            if value == elt[0]:
                return True
        return False
