from rest_framework import status

from api.tests.base import *
from api.views import HealthCheckView


class HealthCheckTestCase(ApiTestCase):

    def test_health(self):
        request = self.factory.get("/api/health/")
        response = HealthCheckView.as_view()(request)
        self.assertTrue(status.is_success(response.status_code))
