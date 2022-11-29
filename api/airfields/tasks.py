from django.apps import apps
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from constance import config

from api.utils import get_current_airac_cycle_date


def get_airfield_model():
    return apps.get_model(app_label="airfields", model_name="Airfield")


def get_airfieldmap_model():
    return apps.get_model(app_label="airfields", model_name="AirfieldMap")


def get_airfieldfrequency_model():
    return apps.get_model(app_label="airfields", model_name="AirfieldFrequency")


def pull_airfields(session):
    Airfield = get_airfield_model()
    AirfieldFrequency = get_airfieldfrequency_model()
    url = "{}api/airfields/airfield/".format(config.FALLBACK_URL)
    r = session.get(url, verify=False)
    for airfield_data in r.json():
        airfield, created = Airfield.objects.update_or_create(icao_code=airfield_data['icao_code'], defaults={
            'name': airfield_data['name'],
            'latitude': int(airfield_data['latitude']['float']*3600),
            'longitude': int(airfield_data['longitude']['float']*3600),
            'category': airfield_data['category']
        })
        print("{} {}".format(
            airfield_data['icao_code'], "CREATED" if created else "UPDATED"))
        airac = get_current_airac_cycle_date()
        if 'frequencies' in airfield_data:
            AirfieldFrequency.objects.filter(airfield=airfield).all().delete()
        for f in airfield_data.get('frequencies', []):
            AirfieldFrequency.objects.create(
                value=f['value'], airfield=airfield,
                frequency_type=f['frequency_type'],
                comments=f['comments'],
                airac=airac
            )
            print("{} ({}) CREATED".format(f['value'], f['frequency_type']))


def pull_airfields_maps(session):
    Airfield = get_airfield_model()
    AirfieldMap = get_airfieldmap_model()
    page_url = "{}api/airfields/map/?page=1".format(config.FALLBACK_URL)
    while page_url:
        r = session.get(page_url, verify=False)
        data = r.json()
        page_url = data.get('next', None)
        for map_data in data['results']:
            try:
                airfield = Airfield.objects.get(
                    icao_code=map_data['airfield'].split(" ")[0])
                map, _ = AirfieldMap.objects.get_or_create(
                    airfield=airfield, name=map_data['name'])
                map.airac = map_data['airac']
                map.save()
                map_filepath = map_data['pdf'].split("media/")[-1]
                if not default_storage.exists(map_filepath):
                    f = session.get(map_data['pdf'], verify=False)
                    map.pdf.save(map_filepath, ContentFile(f.content))
                    print(
                        "{} - {} DOWNLOADED".format(map_data['airfield'], map_data['name']))
                else:
                    print(
                        "{} - {} EXISTS".format(map_data['airfield'], map_data['name']))
            except Exception as e:
                print(
                    "{} - {} FAILED ({})".format(map_data['airfield'], map_data['name'], e))
