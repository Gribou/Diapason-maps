from rest_framework import status

from api.tests.base import *
from .models import Airfield, AirfieldMap
from .views import AirfieldViewSet, AirfieldMapViewSet


class AirfieldApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.airfield = Airfield.objects.create(icao_code="LFPG", name="CDG")
        AirfieldMap.objects.create(
            airfield=self.airfield, airac="2019-01-01", name="Map 1", pdf=generate_uploaded_file())

    def test_read_airfield(self):
        request = self.factory.get("/api/airfields/LFPG/")
        response = AirfieldViewSet.as_view(
            {'get': 'retrieve'})(request, icao_code="LFPG")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["icao_code"], "LFPG")
        self.assertEqual(response.data['maps'][0]['name'], "Map 1")

    def test_read_wrong_airfield(self):
        request = self.factory.get("/api/airfields/XXXX/")
        response = AirfieldViewSet.as_view(
            {'get': 'retrieve'})(request, icao_code="XXXX")
        self.assertTrue(status.is_client_error(response.status_code))

    def test_search_airfield(self):
        request = self.factory.get("/api/airfields/", {'search': "CDG"})
        response = AirfieldViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data[0]['icao_code'], 'LFPG')

    def test_search_map(self):
        request = self.factory.get("/api/maps/", {'search': "CDG"})
        response = AirfieldMapViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Map 1')

    def test_search_map_no_results(self):
        request = self.factory.get("/api/maps/", {'search': "Bad"})
        response = AirfieldMapViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['count'], 0)
