from rest_framework import status
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import shutil
import os

from api.tests.base import *
from .views import TelephoneCategoryViewSet, TelephoneViewSet
from .tasks import import_csv_phonebook
from .models import Telephone, TelephoneCategory


class PhoneApiViewsTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        cat1 = TelephoneCategory.objects.create(name="Cat1")
        cat2 = TelephoneCategory.objects.create(name="Cat2")
        Telephone.objects.create(
            name="Phone1", category=cat1, alias="Téléphone1")
        Telephone.objects.create(name="Phone2", category=cat2)
        Telephone.objects.create(name="Phone3", category=cat2, alias="Tsouin")

    def test_list_categories(self):
        request = self.factory.get("/api/phones/category/")
        response = TelephoneCategoryViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 2)

    def test_list_phones(self):
        request = self.factory.get("/api/phones/phone/")
        response = TelephoneViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 3)

    def test_search_phones(self):
        request = self.factory.get("/api/phones/phone/", {"search": "tsouin"})
        response = TelephoneViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Phone3")


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class TelephoneImportTestCase(TestCase):

    def setUp(self):
        super().setUp()
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_import_phones(self):
        self.phonebook_path = default_storage.path("phones_test.csv")
        default_storage.save(self.phonebook_path, open(
            finders.find("tests/phones_test.csv"), "rb"))
        import_csv_phonebook(self.phonebook_path)
        self.assertEqual(TelephoneCategory.objects.count(), 3)
        self.assertEqual(Telephone.objects.count(), 126)
        self.assertFalse(default_storage.exists(self.phonebook_path))

    def test_import_fails_with_non_csv_file(self):
        self.phonebook_path = default_storage.path(
            "phones_test_with_errors.csv")
        default_storage.save(self.phonebook_path, ContentFile(b'bad file'))
        with self.assertRaises(ValueError):
            import_csv_phonebook(self.phonebook_path)
        self.assertEqual(TelephoneCategory.objects.count(), 0)
        self.assertEqual(Telephone.objects.count(), 0)
        self.assertFalse(default_storage.exists(self.phonebook_path))

    def test_import_fails_with_incorrect_headers(self):
        self.phonebook_path = default_storage.path("phones_test.csv")
        default_storage.save(self.phonebook_path, open(
            finders.find("tests/phones_bad.csv"), "rb"))
        with self.assertRaises(ValueError):
            import_csv_phonebook(self.phonebook_path)
        self.assertEqual(TelephoneCategory.objects.count(), 0)
        self.assertEqual(Telephone.objects.count(), 0)
        self.assertFalse(default_storage.exists(self.phonebook_path))
