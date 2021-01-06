from django.urls import path,include
from django.views.generic import TemplateView

from . import views

app_name = 'web'
urlpatterns = [
    path(r'', views.home, name='home'),
	path(r'analyze', views.analyze, name='analyze'),
	path(r'options', views.options, name='options'),
	path(r'resources', views.resources, name='resources'),
	path('', include('stock_analyzer.urls')),
    path(r'terms', TemplateView.as_view(template_name="web/terms.html"), name='terms'),
]
