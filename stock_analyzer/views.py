from django.shortcuts import render
import requests,csv, tweepy
from . import  Util as u, Config as config
from urllib.parse import urlparse
from rest_framework import generics
from django.http import JsonResponse
from celery import shared_task
from .models import StockAnalyzer
import json
from .serializers import StockAnalyzerSerializer
from rest_framework.authtoken.models import Token
from django.core import serializers
# Create your views here.
class ListStockAnalyzerView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = StockAnalyzerSerializer
    def get(request):
        queryset = StockAnalyzer.objects.all()

def get_latest_Record(request):
    new_record = StockAnalyzer.objects.latest('id')
    keyword= new_record.keyword
    account_count=new_record.account_count
    stock_id=new_record.stock_id
    screen_name=new_record.screen_name
    url=new_record.url
    email=new_record.email
    data ={
        'keyword':keyword,
        'account_count':account_count,
        'stock_id':stock_id,
        'keyword':keyword,
        'screen_name':screen_name,
        'url':url,
        'email':email,
    }
    # data = serializers.serialize('json', new_record)
    return JsonResponse(data,safe=False)
@shared_task
def generalist(request):
    api_key = config.api_key
    api_secret = config.api_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    query = request.POST['ticker']
    avoid = request.POST.get('email_exclude', '')=='on'
    save = True

    account_count = 0
    ids = []

    filter_list = u.getFilterList()

    keywords = query.split(",")

    if avoid == "True":
        avoid = True
        print(avoid)

    for keyword in keywords:
        accounts = tweepy.Cursor(api.search_users, keyword).pages(51)
        keyword = keyword.lstrip()

        for page in accounts:
            for account in page:
                id = account.id_str
                emails = []
                new_emails = []

                if id not in ids:
                    screen_name = account.screen_name

                    try:
                        r = requests.get(account.url)
                        new_url = r.url
                        url = "https://" + urlparse(new_url).netloc

                        try:
                            emails = u.emailExtractor(url)
                            validity = True

                            for email in emails:
                                email = str(email).replace("thello", "hello").replace("tsupport", "support").replace(
                                    "tinfo", "info")

                                for word in filter_list:
                                    if word in email:
                                        validity = False

                                if validity:
                                    email = email.lower()
                                    new_emails.append(email)

                            new_emails = list(dict.fromkeys(new_emails))

                        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                            print("(" + keyword + " #" + str(
                                account_count) + "): " + id + " | " + screen_name + " | " + url)
                            continue

                        account_count += 1

                        with open("Contacts.csv", "a", newline='') as contacts:
                            writer = csv.writer(contacts, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                            if len(new_emails) > 0:
                                print("(" + keyword + " #" + str(
                                    account_count) + "): " + id + " | " + screen_name + " | " + url + " | " + str(
                                    new_emails))
                                # save records to db
                                stocks=StockAnalyzer.objects.create(keyword=keyword,account_count=account_count,stock_id=id,screen_name=screen_name,url=url,email=new_emails)
                                stocks.save()
                                data = serializers.serialize('json', stocks)
                                return JsonResponse(data ,safe=False)

                                for email in new_emails:
                                    writer.writerow([id, screen_name, url, email])
                            else:
                                if not avoid:
                                    print("(" + keyword + " #" + str(
                                        account_count) + "): " + id + " | " + screen_name + " | " + url + " | (/)")
                                    stocks = StockAnalyzer.objects.create(keyword=keyword, account_count=account_count,
                                                                          stock_id=id, screen_name=screen_name, url=url,
                                                                          email=new_emails)
                                    stocks.save()
                                    data = serializers.serialize('json', stocks)
                                    return JsonResponse(data, safe=False)
                                    writer.writerow([id, screen_name, url, "-"])

                            ids.append(id)

                    except:
                        url = "(/)"

    return JsonResponse("test")
