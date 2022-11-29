from api.utils import get_current_airac_cycle_date
from scraper.boundaries import process_raw_boundaries

from .items import AzbaScheduleItem, AzbaKnownScheduleItem, AzbaAreaItem
from ..models import AzbaKnownSchedule, AzbaSchedule, AzbaArea


class AzbaPipeline:

    def process_item(self, item, spider):
        if isinstance(item, AzbaScheduleItem):
            self._process_azba_schedule(item)
        if isinstance(item, AzbaKnownScheduleItem):
            self._process_azba_known_schedule(item)
        if isinstance(item, AzbaAreaItem):
            self._process_azba_area(item)
        return item

    def _process_azba_known_schedule(self, item):
        if item.get('up_to', None):
            AzbaKnownSchedule.objects.create(
                up_to=item['up_to'], from_d=item['from_d'])
        # FIXME else raise error ?

    def _process_azba_schedule(self, item):
        azba_name = item.pop('azba', None)
        if azba_name:
            azba = AzbaArea.objects.filter(slug=azba_name)
            # TODO startswith ?
            if not azba.exists():
                azba = AzbaArea.objects.create(
                    slug=azba_name, label=azba_name, airac=get_current_airac_cycle_date())
            else:
                azba = azba.first()
            AzbaSchedule.objects.update_or_create(azba=azba, **item)
        # no need to ensure unicity if only the active/inactive status is exposed

    def _process_azba_area(self, item):
        slug = item['label'].replace(" ", "")
        azba, _ = AzbaArea.objects.get_or_create(
            slug=slug, defaults={'label': item['label'], 'airac': item['airac']})
        azba.label = item['label']
        azba.ceiling = item['ceiling']
        azba.floor = item['floor']
        azba.airac = item['airac']
        azba.boundaries = process_raw_boundaries(item['boundaries'])
        azba.save()
