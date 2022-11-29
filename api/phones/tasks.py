
from celery import shared_task
from django.apps import apps
from django.core.files.storage import default_storage
import csv

CSV_HEADERS = ['Categorie', 'Rang', 'Plage', 'Numero_court', 'Nom',
               'Numero_long', 'Exterieur', 'Montrer_CDS', 'Montrer_W', 'Montrer_E', 'Alias']


def _get_phone_model():
    return apps.get_model(app_label="phones", model_name="Telephone")


def _get_category_model():
    return apps.get_model(app_label="phones", model_name="TelephoneCategory")


def csv_checker(csv_reader):
    # If csv_reader has fieldnames -> can check
    # Checks that every csv file column name corresponds to the CSV_HEADERS
    for h in CSV_HEADERS:
        if h != "" and h not in csv_reader.fieldnames:
            raise ValueError("Headers should be {}".format(
                ", ".join(CSV_HEADERS)))


@shared_task
def import_csv_phonebook(uploaded_file_name):
    Telephone = _get_phone_model()
    TelephoneCategory = _get_category_model()
    file_path = default_storage.path(uploaded_file_name)
    try:
        with open(file_path, 'r', encoding='iso-8859-1') as csv_file:
            decoded_file = csv_file.read().splitlines()
            csv_reader = csv.DictReader(decoded_file, delimiter=';')
            telephone_list = []
            telephone_category = {}
            category = ''
            # Check if data header is OK before deleting table -> raise exception if not
            csv_checker(csv_reader)
            for row in csv_reader:
                # If category is present => store value
                if len(row[CSV_HEADERS[0]]) > 0:
                    category_name = row[CSV_HEADERS[0]]
                    category = TelephoneCategory.objects.update_or_create(
                        name=category_name, defaults={'rank': int(row[CSV_HEADERS[1]])})
                    telephone_category[category_name] = category[0]
                # General case : store data if present
                if len(CSV_HEADERS[4]) > 0 and len(row[CSV_HEADERS[3]]) > 0:
                    telephone = Telephone(
                        name=row[CSV_HEADERS[4]],
                        category=telephone_category[category_name],
                        telephone_number=row[CSV_HEADERS[3]],
                        isExterior=1 if row[CSV_HEADERS[6]
                                            ] == 'oui' else 0,
                        isCDS=1 if row[CSV_HEADERS[7]
                                       ] == 'oui' else 0,
                        isW=1 if row[CSV_HEADERS[8]] == 'oui' else 0,
                        isE=1 if row[CSV_HEADERS[9]] == 'oui' else 0,
                        alias=row[CSV_HEADERS[10]])
                    telephone_list.append(telephone)
            if len(telephone_list) > 0:  # There is data to store
                # Delete table content
                Telephone.objects.all().delete()
                # Fill table with fresh data
                Telephone.objects.bulk_create(telephone_list)
                print("Votre fichier a été importé, {} ajouts".format(
                    len(telephone_list)))
            else:
                print("Votre fichier a été importé, mais aucune donnée n'a été ajoutée")
    finally:
        default_storage.delete(uploaded_file_name)
