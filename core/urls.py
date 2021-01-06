"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls, get_schemajs_view
from django.views.static import serve 

schemajs_view = get_schemajs_view(title="API")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('', include('apps.web.urls')),
    path('pegasus/', include('pegasus.apps.examples.urls')),
    path('celery-progress/', include('celery_progress.urls')),
    # API docs
    # these are needed for schema.js
    path('docs/', include_docs_urls(title='API Docs')),
    path('schemajs/', schemajs_view, name='api_schemajs'),

    # djstripe urls - for webhooks
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # stock_analyzer app urls
    path('api/stocks/', include('stock_analyzer.urls',namespace='api-stocks')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
