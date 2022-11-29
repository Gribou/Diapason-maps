from django.db import router
from django.urls import path, include
from django.shortcuts import redirect

from airfields.urls import router as airfields_router
from civ.urls import router as civ_router
from acc.urls import router as acc_router
from phones.urls import router as phones_router
from files.urls import router as files_router
from nav.urls import router as nav_router
from tiles.urls import router as tiles_router
from radionav.urls import router as radionav_router

from .routers import NestedDefaultRouter
from .views import InfoView, HealthCheckView

router = NestedDefaultRouter()
router.register_nested_router("airfields", airfields_router)
router.register_nested_router("civ", civ_router)
router.register_nested_router("acc", acc_router)
router.register_nested_router("radionav", radionav_router)
router.register_nested_router("phones", phones_router)
router.register_nested_router("files", files_router)
router.register_nested_router("nav", nav_router)
router.register_nested_router("layers", tiles_router)
router.register_additional_view("info", "api-info")
router.register_additional_view("login", "api-login")
router.register_additional_view("logout", "api-logout")
router.register_additional_view("health", "api-health")


def api_root(req): return redirect("api-root")


urlpatterns = [
    path('', include(router.urls)),
    path('info/', InfoView.as_view(), name='api-info'),
    # redirect nested root views to API root
    path('phones/', api_root),
    path('civ/', api_root),
    path('acc/', api_root),
    path('phones/', api_root),
    path('files/', api_root),
    path('radionav/', api_root),
    path('nav/', api_root),
    path('airfields/', api_root),
    path('layers/', api_root),
    path('health/', HealthCheckView.as_view(),
         name="api-health"),
]
