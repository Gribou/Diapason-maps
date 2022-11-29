from django.urls import path

from .views import LogoutView, StandaloneLoginView

app_name = "sso"
urlpatterns = [
    path('account/token/logout/', LogoutView.as_view(), name='api-logout'),
    path('account/token/login/',
         StandaloneLoginView.as_view(), name='api-login'),
]
