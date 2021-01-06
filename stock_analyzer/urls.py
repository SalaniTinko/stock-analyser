from django.urls import path, include, re_path
from . import views
from . import views
from stock_analyzer.views import  ListStockAnalyzerView

app_name ="sa" #app name sa -> "stock analyzer"
urlpatterns = [
    path('genralist/',views.generalist,name="genralist"),
    path('get-latest-Record/',views.get_latest_Record,name="get-latest-Record"),
    path('', ListStockAnalyzerView.as_view(),name="stock-list"),
]