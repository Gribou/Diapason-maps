from django.apps import apps
from constance import config

from api.utils import get_current_airac_cycle_date


def get_radionav_model():
    return apps.get_model(app_label="radionav", model_name="RadioNavStation")


def get_radionavtype_model():
    return apps.get_model(app_label="radionav", model_name="RadioNavType")


def pull_radionav(session):
    RadioNavStation = get_radionav_model()
    RadioNavType = get_radionavtype_model()
    url = "{}api/radionav/station/".format(config.FALLBACK_URL)
    r = session.get(url, verify=False)
    for station_data in r.json():
        station, created = RadioNavStation.objects.update_or_create(
            short_name=station_data['short_name'], defaults={
                'long_name': station_data['long_name'],
                'frequency': station_data['frequency'],
                'latitude': int(station_data['latitude']['float']*3600),
                'longitude': int(station_data['longitude']['float']*3600),
                'range': station_data['range'],
                'airac': get_current_airac_cycle_date()
            })
        station.types.set([RadioNavType.objects.get_or_create(
            label=l)[0] for l in station_data['types']])
        print("{} {}".format(
            station_data['short_name'], "CREATED" if created else "UPDATED"))
