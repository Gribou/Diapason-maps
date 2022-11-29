from rest_framework import status

from api.tests.base import *
from .models import Antenna, Sector, ControlCenter
from .views import AntennaViewSet, SectorViewSet, ControlCenterViewSet


class AntennaApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        Antenna.objects.create(name="TST")

    def test_list_antenna(self):
        request = self.factory.get("/api/antennas/")
        response = AntennaViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data[0]['name'], 'TST')


class ControlCenterApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        cc = ControlCenter.objects.create(name="TEST ACC")
        Sector.objects.create(name="TT", control_center=cc)
        ControlCenter.objects.create(name="OTHER")

    def test_list_acc(self):
        request = self.factory.get("/api/acc/")
        response = ControlCenterViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['name'], 'TEST ACC')
        self.assertEqual(response.data[1]['sectors'][0]['name'], 'TT')

    def test_search_acc(self):
        request = self.factory.get("/api/acc/", {'search': "OTHER"})
        response = ControlCenterViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'OTHER')
        self.assertEqual(response.data[0]['sectors'], [])


class SectorApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        cc = ControlCenter.objects.create(name="TEST ACC")
        Sector.objects.create(name="TT", control_center=cc)
        Sector.objects.create(name="AP", control_center=cc)

    def test_read_sector(self):
        request = self.factory.get("/api/sectors/TT/")
        response = SectorViewSet.as_view(
            {"get": "retrieve"})(request, name="TT")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['name'], 'TT')
        self.assertEqual(
            response.data['control_center'], 'TEST ACC')
        self.assertEqual(response.data['parts'], [])

    def test_search_sector(self):
        request = self.factory.get("/api/sectors/", {'search': "AP"})
        response = SectorViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'AP')

        request = self.factory.get("/api/sectors/", {'search': "BAD"})
        response = SectorViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 0)
