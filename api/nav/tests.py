from rest_framework import status

from api.tests.base import *
from .populate import populate
from .models import HomePageItem, Shortcut
from .views import HomePageItemViewSet, ToolbarItemViewSet


class NavViewsApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        populate()

    def test_toolbar_view(self):
        request = self.factory.get("/api/nav/toolbar/")
        response = ToolbarItemViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual([i['shortcut']['label']
                         for i in response.data], ['CIV', 'Carte'])

    def test_homepage_view(self):
        HomePageItem.objects.create(
            shortcut=Shortcut.objects.get(url="/telephones"), rank=0)
        HomePageItem.objects.create(
            shortcut=Shortcut.objects.get(url="/files"), rank=1)
        request = self.factory.get("/api/nav/homepage/")
        response = HomePageItemViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual([i['shortcut']['label']
                         for i in response.data], ['Téléphones', 'Fichiers'])
