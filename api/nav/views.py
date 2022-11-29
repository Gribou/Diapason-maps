from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import HomePageItemSerializer, ToolbarItemSerializer
from .models import HomePageItem, ToolbarItem


class HomePageItemViewSet(ReadOnlyModelViewSet):
    serializer_class = HomePageItemSerializer
    queryset = HomePageItem.objects.all()


class ToolbarItemViewSet(ReadOnlyModelViewSet):
    serializer_class = ToolbarItemSerializer
    queryset = ToolbarItem.objects.all()
