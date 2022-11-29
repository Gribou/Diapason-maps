from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


from api.tests.base import *
from .models import FileCategory, StaticFile
from .views import FileCategoryViewSet, StaticFileViewSet


class FiletreeApiTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        cat1 = FileCategory.objects.create(label='cat1')
        cat2 = FileCategory.objects.create(label="cat2")
        self.f1 = StaticFile.objects.create(
            label="file1", pdf=generate_uploaded_file())
        f2 = StaticFile.objects.create(
            label="file2", pdf=generate_uploaded_file())
        f3 = StaticFile.objects.create(
            label="file3", pdf=generate_uploaded_file())
        cat1.files.set([self.f1, f2])
        cat2.files.set([f3])
        self.editor_user = get_user_model().objects.create_user(
            username="editor", password="editor")
        self.editor_user.user_permissions.add(
            Permission.objects.get(codename="add_staticfile"))
        self.editor_user.user_permissions.add(
            Permission.objects.get(codename="add_filecategory"))

    def test_list_category(self):
        request = self.factory.get("/api/files/category/")
        response = FileCategoryViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['label'], 'cat1')
        self.assertEqual(response.data[1]['label'], 'cat2')

    def test_list_files(self):
        request = self.factory.get("/api/files/")
        response = StaticFileViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['label'], 'file1')
        self.assertEqual(response.data[1]['label'], 'file2')
        self.assertEqual(response.data[2]['label'], 'file3')

    def test_search_files(self):
        request = self.factory.get("/api/files/", {"search": "3"})
        response = StaticFileViewSet.as_view({"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'file3')

    def test_create_file(self):
        request = self.factory.post(
            "/api/files/", {"label": "LABEL", "pdf": generate_uploaded_file()}, format="multipart")
        response = StaticFileViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.editor_user)
        response = StaticFileViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(StaticFile.objects.count(), 4)

    def test_create_file_fails_if_not_pdf(self):
        request = self.factory.post(
            "/api/files/", {"label": "LABEL", "pdf": generate_uploaded_file(title="bad.txt")}, format="multipart")
        force_authenticate(request, user=self.editor_user)
        response = StaticFileViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_category(self):
        request = self.factory.post("/api/files/category/", {"label": "LABEL"})
        response = FileCategoryViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.editor_user)
        response = FileCategoryViewSet.as_view({"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(FileCategory.objects.count(), 3)
