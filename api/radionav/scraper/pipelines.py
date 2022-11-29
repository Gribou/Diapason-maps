from scraper.clean import clean_latitude, clean_longitude

from .items import RadioNavStationItem
from ..models import RadioNavStation, RadioNavType


class RadionavPipeline:
    def process_item(self, item, spider):
        if isinstance(item, RadioNavStationItem):
            self._process_types(item)
            self._process_station(item)
        return item

    def _process_types(self, item):
        for l in item['types'].split('-'):
            if not RadioNavType.objects.filter(label=l).exists():
                RadioNavType.objects.create(label=l)

    def _process_station(self, item):
        if item['short_name']:
            station, _ = RadioNavStation.objects.update_or_create(
                short_name=item['short_name'], defaults={
                    'long_name': item['long_name'],
                    'frequency': item['frequency'] if "TACAN" not in item['types'] else None,
                    'range': item.get('range', None),
                    'latitude': clean_latitude(item['latitude']),
                    'longitude': clean_longitude(item['longitude']),
                    'airac': item['airac']
                }
            )
            for l in item['types'].split('-'):
                t = RadioNavType.objects.get(label=l)
                if t not in station.types.all():
                    station.types.add(t)
            # FIXME : a station can have multiple
