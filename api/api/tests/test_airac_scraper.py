from api.tests.base import *
from api.tasks import download_last_airac

from airfields.models import Airfield
from acc.models import Sector

# FIXME use a mock or a partial mode instead of really scraping the entire data
# @override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
# class CivScraperTestCase(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         logging.disable(logging.ERROR)
#         download_last_airac()  # NOTE: do this only ONCE !

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         if "twisted.internet.reactor" in sys.modules:
#             del sys.modules["twisted.internet.reactor"]
#         logging.disable(logging.NOTSET)
#         try:
#             shutil.rmtree(MEDIA_ROOT_TEST)
#         except OSError:
#             pass

#     def test_french_airfields_were_scraped(self):
#         self.assertTrue(Airfield.objects.filter(
#             icao_code__startswith="LF").count() > 50)
#         lfpg = Airfield.objects.get(icao_code="LFPG")
#         self.assertTrue(lfpg.maps.exists())
#         self.assertTrue(lfpg.frequencies.exists())

#     def test_british_airfields_were_scraped(self):
#         self.assertTrue(Airfield.objects.filter(
#             icao_code__startswith="EG").count() > 5)

#     def test_belgo_airfields_were_scraped(self):
#         self.assertTrue(Airfield.objects.filter(
#             icao_code__startswith="EB").count() > 5)

#     def test_acc_sectors_were_scraped(self):
#         self.assertTrue(Sector.objects.count() > 20)
#         ap = Sector.objects.get(name="AP")
#         self.assertEqual(ap.control_center.name, "PARIS ACC")
#         self.assertTrue(ap.parts.first().boundaries.exists())
#         self.assertTrue(ap.frequencies.exists())
