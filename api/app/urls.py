"""coconut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import reverse
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect

index = never_cache(TemplateView.as_view(template_name="index.html"))

urlpatterns = [
    path('sso/', include('sso.admin.urls')),
    path('admin/logout/', lambda request: redirect(reverse('sso:logout'),
         permanent=False)),  # uses SSO logout in admin
    path('admin/', admin.site.urls),
    path('admin', RedirectView.as_view(pattern_name='admin:index',
         permanent=False)),  # force trailing slash
    path('api/', include('api.urls')),
    path('api', RedirectView.as_view(pattern_name='api-root',
         permanent=False)),  # force trailing slash
    path('', index, name="home")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

urlpatterns.append(path('<path:path>', index))
