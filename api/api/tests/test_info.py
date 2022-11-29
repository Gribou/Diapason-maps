from rest_framework import status

from api.tests.base import *
from api.views import InfoView


class InfoApiTestCase(ApiTestCase):

    def test_info_view(self):
        request = self.factory.get('/api/info/')
        response = InfoView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data['email_admin'], 'root@localhost')
