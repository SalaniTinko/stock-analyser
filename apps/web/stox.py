from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data
import sys
import requests
import json
from plotly.offline import plot
import plotly.graph_objs as go
import base64
import requests_cache
import datetime
# import statsmodels

wholeday = datetime.timedelta(hours=8)
oneweek = datetime.timedelta(days=7)
onemonth = datetime.timedelta(days=30)

daysession = requests_cache.CachedSession(cache_name='day',
                                       backend='sqlite',
                                       expire_after=wholeday)

weeksession = requests_cache.CachedSession(cache_name='week',
                                       backend='sqlite',
                                       expire_after=oneweek)

monthsession = requests_cache.CachedSession(cache_name='month',
                                       backend='sqlite',
                                       expire_after=onemonth)

# Setup client
# finnhub_client = finnhub.Client(api_key="bt9j16748v6pstot1a0g")


def price():
	return ticker.get_price()

def stats(ticker):
	stat = ticker.get_quote(displayPercent=True)
	stats = {
	'symbol': stat['symbol'],
	'name': stat['companyName'],
	'high': stat['high'],
	'low': stat['low'],
	'1dpchange': round(stat['changePercent'],2),
	'1dchange': stat['change'],
	'1ychange': round(stat['ytdChange'],2),
	'peRatio': stat['peRatio'],
	'1yhigh': stat['week52High'],
	'1ylow': stat['week52Low']
	}
	return stats

def getlogo(ticker):
	return ticker.get_logo()['url']

def pricetarget(ticker):
	target = ticker.get_price_target()
	if target != None:
		targets = {
		'updated': target['updatedDate'],
		'average': target['priceTargetAverage'],
		'low': target['priceTargetLow'],
		'high': target['priceTargetHigh'],
		'currency': target['currency']
		}
		return target
	return None

def news(ticker):
	news = ticker.get_news(last=5)
	return news

def movement(ticker):
	stat = ticker.get_key_stats()
	stats = {
	'earnings': stat['nextEarningsDate'],
	'dividend': stat['exDividendDate'],
	'1wchange': round(stat['day5ChangePercent']*100,2),
	'1mchange': round(stat['month1ChangePercent']*100,2),
	'3mchange': round(stat['month3ChangePercent']*100,2),
	'6mchange': round(stat['month6ChangePercent']*100,2),
	'200mavg': stat['day200MovingAvg'],
	'50mavg': stat['day50MovingAvg'],
	'marketcap': stat['marketcap'],
	'beta': round(stat['beta'],2)
	}
	return stats

def rsi(stock):

	r = daysession.get('https://cloud.iexapis.com/v1/stock/%s/indicator/rsi?token=sk_d39914f003324ad4897db824371876a9&range=1m&period=14' % stock)
	data = json.loads(r.content)
	return round(data['indicator'][0][-1],2)

def fivesma(stock):
	#get 5 day SMA, return last in list
	r = daysession.get('https://cloud.iexapis.com/v1/stock/%s/indicator/sma?token=sk_d39914f003324ad4897db824371876a9&range=5d' % stock)
	data = json.loads(r.content)
	return round(data['indicator'][0][-1],2)

def twentysma(stock):
	#load one months worth of SMAs and move backwards
	r = daysession.get('https://cloud.iexapis.com/v1/stock/%s/indicator/sma?token=sk_d39914f003324ad4897db824371876a9&range=1m' % stock)
	data = json.loads(r.content)
	return round(data['indicator'][0][-9],2)

def fivema(stock):
	#get 5 day EMA, return last in list
	r = daysession.get('https://cloud.iexapis.com/v1/stock/%s/indicator/ema?token=sk_d39914f003324ad4897db824371876a9&range=5d' % stock)
	data = json.loads(r.content)
	return round(data['indicator'][0][-1],2)

def twentyema(stock):
	#load one months worth of EMAs and move backwards
	r = daysession.get('https://cloud.iexapis.com/v1/stock/%s/indicator/ema?token=sk_d39914f003324ad4897db824371876a9&range=1m' % stock)
	data = json.loads(r.content)
	return round(data['indicator'][0][-9],2)


def resistance(stock):
	return finnhub_client.support_resistance(stock, 'D')

def chart(ticker,time):
	chart = ticker.get_chart(range=time,chartCloseOnly=True)
	x = []
	y = []
	for day in chart:
		x.append(day['date'])
		y.append(day['close'])
	fig = go.Figure()

	scatter = go.Scatter(x=x, y=y,mode='lines', name='test',opacity=0.8, marker_color='green')
	fig.add_trace(scatter)
	fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,height=355,width=700,margin=dict(l=1,r=1,b=1,t=1))
	img = fig.to_image(format="svg", engine="kaleido")
	img = base64.b64encode(img)
	return img.decode('utf-8')


def check(tick):
	# 
	ticker = Stock(tick)
	dayticker = Stock(tick)
	weekticker = Stock(tick,session=weeksession)
	monthticker = Stock(tick,session=monthsession)

	stockdata = {
	"price":ticker.get_price(),
	"news":news(dayticker),
	"technical":
	{
	"rsi": rsi(tick),
	"20ema":twentyema(tick),
	"20sma":twentysma(tick),
	"5ema":fivema(tick),
	"5sma":fivesma(tick),
	},
	"stats":stats(ticker),
	"movement":movement(dayticker),
	"logo":getlogo(monthticker),
	"pricetarget":pricetarget(dayticker),
	"1wchart":chart(dayticker,'5d'),
	"1mchart":chart(dayticker,'1m'),
	"3mchart":chart(dayticker,'3m')

	}
	
	return(stockdata)

def valid(tick):
	ticker = Stock(tick,session=monthsession)
	return ticker.get_price()