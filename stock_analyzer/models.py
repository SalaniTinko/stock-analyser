from django.db import models
class StockAnalyzer(models.Model):
    keyword = models.CharField(max_length=50 ,blank=True ,null=True)
    account_count = models.IntegerField(blank=True ,null=True)
    stock_id = models.IntegerField(blank=True ,null=True)
    screen_name = models.CharField(max_length=50 ,blank=True ,null=True)
    url = models.CharField(max_length=100 ,blank=True ,null=True)
    email = models.EmailField(max_length=50 ,blank=True ,null=True)
# Create your models here.
