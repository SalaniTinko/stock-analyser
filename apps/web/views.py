from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .stox import check,valid
from apps.users.forms import StockTicker
import requests
import json
from django.contrib import messages
# from django.views.decorators.csrf import csrf_protect
# from django.template import RequestContext
from .free import allowed

def home(request):
    if request.user.is_authenticated:

        return render(request, 'web/app_home.html', context={
            'active_tab': 'dashboard',
        })

    else:
        return render(request, 'web/landing_page.html')

def analyze(request):
	if request.method == 'POST':
		if allowed(request):
			form = StockTicker(request.POST)
			stock = request.POST['ticker']
			if form.is_valid():
				try:
					valid(stock)
					return render(request, 'web/analyzer.html', context={
						'active_tab': 'dashboard','data':check(stock),'form':form})
				except Exception as e:
					capture_message(str(e), level="error")
					messages.warning(request, 'Invalid Stock Ticker')
		if allowed(request) == False:
			messages.warning(request,'Only 3 requests allowed per day. Please upgrade for unlimited access')
			return render(request, 'web/analyzer.html', context={'active_tab': 'dashboard','form':StockTicker()})
	return render(request, 'web/analyzer.html', context={'active_tab': 'dashboard','form':StockTicker()})

def options(request):
	r = requests.get("https://eodhistoricaldata.com/api/options/AAPL.US?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX")
	data = json.loads(r.content)
	code = data["code"]
	options = data["data"]
	if data["lastTradePrice"] is None:
		price = valid(data["code"])
	else:
		price = data["lastTradePrice"]
	context = {'options':options,'price':price, "code": code}
	return render(request, 'web/options.html',context=context)

def resources(request):
	return render(request, 'web/resources.html')
