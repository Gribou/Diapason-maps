from scraper.boundaries import process_raw_boundaries
from .items import SectorFrequencyItem, SectorPartItem
from ..models import SectorFrequency, ControlCenter, Sector, SectorPart


class SectorFrequencyPipeline:
    def process_item(self, item, spider):
        if isinstance(item, SectorFrequencyItem):
            self._process_sector(item)
        return item

    def _process_sector(self, item):
        # UAC and ACC should be consider the same center
        center, _ = ControlCenter.objects.get_or_create(
            name=item['control_center'].replace("UAC", "ACC"))
        frequency = SectorFrequency.objects.create(
            frequency=item['frequency']['value'],
            frequency_type=item['frequency']['type'],
            airac=item['airac'])
        sector, _ = Sector.objects.get_or_create(name=item['name'])
        sector.control_center = center
        sector.frequencies.add(frequency)
        sector.save()


class SectorPartPipeline:

    def process_item(self, item, spider):
        if isinstance(item, SectorPartItem):
            self._process_part(item)
        return item

    def _process_part(self, item):
        sector_name = self.clean_sector_name(item)
        if sector_name is not None:
            sector, _ = Sector.objects.get_or_create(
                name=sector_name)
            boundaries = process_raw_boundaries(item['boundaries'])
            SectorPart.objects.create(
                sector=sector, airac=item['airac'], ceiling=item['ceiling'], floor=item['floor'], boundaries=boundaries)
        return item

    def clean_sector_name(self, item):
        # LFMM LE sector is split in LE1 and LE2 and then again in 2 parts
        # But frequencies are attributed to LE, not LE1 and LE2
        sector_name = item['sector_name']
        if sector_name in ['LE1', 'LE2']:
            return 'LE'
        return sector_name
