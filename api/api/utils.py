from constance import config
from datetime import date, datetime, timedelta

from airfields.models import AirfieldMap

AIRAC_CYCLE_LENGTH = 28


def get_current_airac_cycle_date():
    ref_date = datetime.strptime(config.AIRAC_REF, '%Y-%m-%d').date()
    nb_cycles_since_ref = (date.today() - ref_date).days // AIRAC_CYCLE_LENGTH
    return ref_date + timedelta(days=nb_cycles_since_ref * AIRAC_CYCLE_LENGTH)


def get_most_recent_airac_in_db():
    try:
        return AirfieldMap.objects.order_by('-airac').first().airac
    except AttributeError:
        return None


def pretty_latitude(latitude):
    degrees = latitude // 3600
    minutes = (latitude % 3600) // 60
    seconds = latitude % 60
    north = 'N' if latitude > 0 else 'S'
    return {
        'display': '{:02d}°{:02d}\'{:02d}"{}'.format(abs(degrees), minutes, seconds, north), 'float': latitude / float(3600)}


def pretty_longitude(longitude):
    degrees = longitude // 3600
    minutes = (longitude % 3600) // 60
    seconds = longitude % 60
    east = 'E' if longitude > 0 else 'W'
    return {'display': '{:03d}°{:02d}\'{:02d}"{}'.format(abs(degrees), minutes, seconds, east), 'float': longitude / float(3600)}
