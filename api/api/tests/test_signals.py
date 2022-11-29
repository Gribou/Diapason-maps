from django.core.files.storage import default_storage

from api.tests.base import *
from files.models import StaticFile


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class FileSignalsTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.f = StaticFile.objects.create(
            label="file1", pdf=generate_uploaded_file())

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_delete_old_file_on_model_update(self):
        current_file = self.f.pdf.path
        self.assertTrue(default_storage.exists(current_file))
        self.f.pdf = generate_uploaded_file(title="other_test.pdf")
        self.f.save()
        self.assertFalse(default_storage.exists(current_file))
        self.assertTrue(default_storage.exists(self.f.pdf.path))

    def test_delete_old_file_on_model_delete(self):
        current_file = self.f.pdf.path
        self.assertTrue(default_storage.exists(current_file))
        self.f.delete()
        self.assertFalse(default_storage.exists(current_file))
