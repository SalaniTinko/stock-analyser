
from rest_framework import serializers
from .models import StockAnalyzer


class StockAnalyzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAnalyzer
        fields = ['keyword', 'account_count', 'stock_id', 'screen_name', 'url', 'email']