import json

from django.contrib import admin
from .models import StockAnalyzer
from django.core.serializers.json import DjangoJSONEncoder



class StockAnalyzerAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', "account_count", "stock_id", "screen_name", "url", "email")
    list_max_show_all = 25
    ordering = ['pk']
    list_filter = ("keyword",)


admin.site.register(StockAnalyzer, StockAnalyzerAdmin)