from rest_framework import status
from rest_framework.test import RequestsClient

from .base import *


class RouterTest(ApiTestCase):

    def test_root_view(self):
        '''API Root View should list all available endpoints'''
        client = RequestsClient()
        response = client.get("http://testserver/api/")
        self.assertTrue(status.is_success(response.status_code))
        content = response.json()
        self.assertTrue(sorted(content.keys()) == sorted([
                        'airfields', 'acc', 'civ', 'phones', 'files', 'nav', 'layers', 'login', 'logout', 'health', 'info', 'radionav']))
