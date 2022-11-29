from django.core.files.storage import default_storage
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
import json

from api.tests.base import *
from .views import MapLayerViewSet
from .models import MapLayer


class TilesViewTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        metadata = {"name": "Test", "type": "overlay", "format": "png",
                    "maxzoom": "9", "minzoom": "1"}
        self.layer = MapLayer.objects.create(
            label="Test", slug="test", metadata=metadata)
        default_storage.save(
            "tiles/test/metadata.json",
            ContentFile(json.dumps(metadata))
        )

        self.editor_user = get_user_model().objects.create_user(
            username="editor", password="editor")
        self.editor_user.user_permissions.add(
            Permission.objects.get(codename="add_maplayer"))
        self.editor_user.user_permissions.add(
            Permission.objects.get(codename="change_maplayer"))
        self.editor_user.user_permissions.add(
            Permission.objects.get(codename="delete_maplayer"))

    def test_list_layers(self):
        request = self.factory.get("/api/layers/layer/")
        response = MapLayerViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slug'], "test")

    def test_hide_layers_without_metadata(self):
        self.layer.metadata = None
        self.layer.save()
        request = self.factory.get("/api/layers/layer/")
        response = MapLayerViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 0)

    def test_read_layer_by_slug(self):
        request = self.factory.get("/api/layers/layer/test/")
        response = MapLayerViewSet.as_view(
            {"get": "retrieve"})(request, slug="test")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["tiles_url"],
                         "http://testserver/media/tiles/test/$Z/$X/$Y.png")

    def test_create_layer(self):
        request = self.factory.post(
            "/api/layers/layer/", {"slug": "test2", "label": "Test2"}, format="multipart")
        response = MapLayerViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.editor_user)
        response = MapLayerViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(MapLayer.objects.filter(slug="test2").exists())

    def test_update_layer(self):
        request = self.factory.put(
            "/api/layers/layer/test/", {"label": "New Label", "slug": "test"}, format="multipart")
        response = MapLayerViewSet.as_view(
            {"put": "update"})(request, slug="test")
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.editor_user)
        response = MapLayerViewSet.as_view(
            {"put": "update"})(request, slug="test")
        self.assertTrue(status.is_success(response.status_code))
        self.layer.refresh_from_db()
        self.assertEqual(self.layer.label, "New Label")

    def test_destroy_layer(self):
        request = self.factory.delete("/api/layers/layer/test/")
        response = MapLayerViewSet.as_view(
            {"delete": "destroy"})(request, slug="test")
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.editor_user)
        response = MapLayerViewSet.as_view(
            {"delete": "destroy"})(request, slug="test")
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(MapLayer.objects.filter(slug="test").exists())


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class TileGenerationTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        with open(finders.find("tests/test.mbtiles"), 'rb') as f:
            self.test_mbfile = SimpleUploadedFile("test.mbtiles", f.read())

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_tile_generation_on_create(self):
        self.layer = MapLayer.objects.create(label="Test", slug="test",
                                             mbtiles_file=self.test_mbfile)
        self.layer.refresh_from_db()
        self.assertFalse(self.layer.mbtiles_file)
        self.assertTrue(self.layer.has_tiles())
        self.assertTrue(default_storage.exists("tiles/test/1/0/0.png"))

    def test_tile_generation_on_update(self):
        self.layer = MapLayer.objects.create(label="Test", slug="test")
        self.layer.refresh_from_db()
        self.assertFalse(self.layer.has_tiles())

        self.layer.mbtiles_file = self.test_mbfile
        self.layer.save()
        self.layer.refresh_from_db()
        self.assertFalse(self.layer.mbtiles_file)
        self.assertTrue(self.layer.has_tiles())
        self.assertTrue(default_storage.exists("tiles/test/1/0/0.png"))

    def test_bad_mbfile_import(self):
        '''tile generation should fail but mbtiles_file should still be deleted'''
        self.layer = MapLayer.objects.create(label="Test", slug="test",
                                             mbtiles_file=SimpleUploadedFile("test.mbtiles", b"bad file"))
        self.layer.refresh_from_db()
        self.assertFalse(self.layer.mbtiles_file)
        self.assertFalse(self.layer.has_tiles())
        self.assertFalse(default_storage.exists("tiles/test/1/0/0.png"))

    def test_tiles_folder_renamed_on_slug_update(self):
        self.layer = MapLayer.objects.create(label="Test", slug="test",
                                             mbtiles_file=self.test_mbfile)
        self.layer.slug = "new_test"
        self.layer.save()
        self.assertTrue(default_storage.exists("tiles/new_test/1/0/0.png"))
        self.assertFalse(default_storage.exists("tiles/test/1/0/0.png"))

    def test_tiles_folder_deleted_on_slug_delete(self):
        self.layer = MapLayer.objects.create(label="Test", slug="test",
                                             mbtiles_file=self.test_mbfile)
        self.layer.delete()
        self.assertFalse(default_storage.exists("tiles/test/1/0/0.png"))


# TODO zip file extraction
