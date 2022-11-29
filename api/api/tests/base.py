from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from contextlib import contextmanager
from django.core.files.uploadedfile import SimpleUploadedFile

import shutil
import lorem

import logging
import sys

from sso.populate import populate as populate_sso


@contextmanager
def streamhandler_to_console(lggr):
    # Use 'up to date' value of sys.stdout for StreamHandler,
    # as set by test runner.
    stream_handler = logging.StreamHandler(sys.stdout)
    lggr.addHandler(stream_handler)
    yield
    lggr.removeHandler(stream_handler)


def testcase_log_console(lggr):
    def testcase_decorator(func):
        def testcase_log_console(*args, **kwargs):
            with streamhandler_to_console(lggr):
                return func(*args, **kwargs)

        return testcase_log_console

    return testcase_decorator


logger = logging.getLogger('django')
# use with @testcase_log_console(logger)

MEDIA_ROOT_TEST = "media_test"


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class ApiTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def setUp(self):
        self.factory = APIRequestFactory()
        populate_sso()


def generate_uploaded_file(title='test.pdf'):
    return SimpleUploadedFile(
        title, lorem.text().encode(), content_type="text/plain")
