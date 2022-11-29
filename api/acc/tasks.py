from django.apps import apps
from constance import config

from api.utils import get_current_airac_cycle_date


def get_frequency_model():
    return apps.get_model(app_label="acc", model_name="SectorFrequency")


def get_part_model():
    return apps.get_model(app_label="acc", model_name="SectorPart")


def get_sector_model():
    return apps.get_model(app_label="acc", model_name="Sector")


def get_control_center_model():
    return apps.get_model(app_label="acc", model_name="ControlCenter")


def pull_sectors(session):
    Sector = get_sector_model()
    ControlCenter = get_control_center_model()
    airac = get_current_airac_cycle_date()
    url = "{}api/acc/sector/?full=true".format(config.FALLBACK_URL)
    r = session.get(url, verify=False)
    for sector_data in r.json():
        control_center, _ = ControlCenter.objects.get_or_create(
            name=sector_data['control_center'])
        sector, created = Sector.objects.get_or_create(
            name=sector_data['name'], control_center=control_center)
        if created:
            print("{} CREATED".format(sector_data['name']))
        create_frequencies_from_data(sector, airac, sector_data['frequencies'])
        create_boundaries_from_data(sector, airac, sector_data['parts'])


def create_frequencies_from_data(sector, airac, data):
    sector.frequencies.clear()
    SectorFrequency = get_frequency_model()
    for f in data:
        SectorFrequency.objects.create(
            frequency=f['frequency'], frequency_type=f['frequency_type'][0], airac=airac)
        print("{} CREATED".format(f['frequency']))


def create_boundaries_from_data(sector, airac, data):
    SectorPart = get_part_model()
    sector.parts.all().delete()
    for i, p in enumerate(data):
        SectorPart.objects.create(sector=sector, airac=airac,
                                  ceiling=p['ceiling'], floor=p['floor'],
                                  boundaries=p['boundaries'])
        print("{} part {} boundary CREATED".format(
            sector.name, i+1))
