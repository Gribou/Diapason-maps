from django.utils import timezone
from datetime import timedelta
from rest_framework import status

from api.tests.base import *
from airfields.models import Airfield
from .models import CivSchedule
from .views import CIVScheduleViewSet


class CivApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        airfield = Airfield.objects.create(icao_code="LFPO", name="LFPO")
        CivSchedule.objects.create(label="CIV LFFF", reference=airfield)
        CivSchedule.objects.create(label="CIV LFMM")

    def test_civ_schedule_list(self):
        request = self.factory.get('/api/civ/')
        response = CIVScheduleViewSet.as_view({'get': 'list'})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['label'], "CIV LFFF")
        self.assertEqual(response.data[1]['label'], "CIV LFMM")

# SIA changed its format. This does not work anymore. 19/07/2022
#@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
#class CivScraperTestCase(TestCase):

#    def setUp(self):
#        logging.disable(logging.ERROR)
#        download_azba()

#    def tearDown(self):
#        logging.disable(logging.NOTSET)
#        if "twisted.internet.reactor" in sys.modules:
#            del sys.modules["twisted.internet.reactor"]
#        try:
#            shutil.rmtree(MEDIA_ROOT_TEST)
#        except OSError:
#            pass

#    def test_azba_were_scraped(self):
#        self.assertTrue(AzbaMap.objects.filter(pdf__isnull=False).exists())
        # FIXME what if no azba map exists on sia.aviation that day ?
