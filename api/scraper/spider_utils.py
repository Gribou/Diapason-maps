import locale
from datetime import datetime

SIA_URL = 'sia.aviation-civile.gouv.fr'

# Root page of eAIP of a given date
ROOT_URL_TEMPLATE = "https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_{}/FRANCE/AIRAC-{}/html/eAIP/"


def get_pretty_airac_date(airac_date):
    current_locale = locale.getlocale()
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    pretty_date = airac_date.strftime("%d_%b_%Y").upper()  # ex : 22_APR_2021
    locale.setlocale(locale.LC_ALL, current_locale)
    return pretty_date


def make_root_url(airac_date):
    data_date = airac_date.strftime("%Y-%m-%d")  # ex : 2021-04-22
    pretty_date = get_pretty_airac_date(airac_date)
    return ROOT_URL_TEMPLATE.format(pretty_date, data_date)


def get_airac_date_from_arg(obj):
    return datetime.strptime(
        getattr(obj, 'airac', None), '%Y-%m-%d').date()


def extract_field_value_from_row(row, field_name):
    return row.css("{}::text, {} ins::text".format(field_name, field_name))

# TODO ?
# ENR2.2 : FRA cells
# ENR4.4 : waypoints coordinates
# ENR3.1/3.2 : airways/PDR
# ENR5.2 : TRA/TSA areas
