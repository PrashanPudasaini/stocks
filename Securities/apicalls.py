import requests
import pandas as pd
from django.http import HttpResponseRedirect
from .models import Market
import datetime
from django.core.files import File

# def get_symbols_list():
#     url_symbols_list = 'https://financialmodelingprep.com/api/v3/stock/list?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
#     symbols_list_json = requests.get(url_symbols_list).json()
#     symbols_list = pd.DataFrame.from_dict(symbols_list_json)
#     print(symbols_list)
#     # market_datetime = datetime.datetime.now()
#     # market_date = market_datetime.strftime("%Y-%m-%d")
#     symbols_list.to_csv("symbols_list", encoding='utf-8', index=False, sep=',')
#     symbols_list_file = open("symbols_list")
#     defaults = dict(
#     # market_date = market_date,
#     symbols_list = File(symbols_list_file)
#     )
#     symbols_list, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
#     return HttpResponseRedirect("/stocks/markets/")


def get_major_indexes():
    url_indexes = 'https://financialmodelingprep.com/api/v3/quotes/index?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    indexes_json = requests.get(url_indexes).json()
    indexes = pd.DataFrame.from_dict(indexes_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    indexes.to_csv("indexes", encoding='utf-8', index=False, sep=',')
    indexes_file = open("indexes")
    defaults = dict(
    market_date = market_date,
    major_indexes = File(indexes_file)
    )
    major_indexes, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_most_active():
    url_most_active = 'https://financialmodelingprep.com/api/v3/actives?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    most_active_json = requests.get(url_most_active).json()
    most_active = pd.DataFrame.from_dict(most_active_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    most_active.to_csv("most_active", encoding='utf-8', index=False, sep=',')
    most_active_file = open("most_active")
    defaults = dict(
    market_date = market_date,
    most_active = File(most_active_file)
    )
    most_active, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_top_gainers():
    url_top_gainers = 'https://financialmodelingprep.com/api/v3/gainers?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    top_gainers_json = requests.get(url_top_gainers).json()
    top_gainers = pd.DataFrame.from_dict(top_gainers_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    top_gainers.to_csv("top_gainers", encoding='utf-8', index=False, sep=',')
    top_gainers_file = open("top_gainers")
    defaults = dict(
    market_date = market_date,
    top_gainers = File(top_gainers_file)
    )
    top_gainers, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_top_losers():
    url_top_losers = 'https://financialmodelingprep.com/api/v3/losers?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    top_losers_json = requests.get(url_top_losers).json()
    top_losers = pd.DataFrame.from_dict(top_losers_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    top_losers.to_csv("top_losers", encoding='utf-8', index=False, sep=',')
    top_losers_file = open("top_losers")
    defaults = dict(
    market_date = market_date,
    top_losers = File(top_losers_file)
    )
    top_losers, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_sector_performance():
    url_sector_performance = 'https://financialmodelingprep.com/api/v3/sectors-performance?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    sector_performance_json = requests.get(url_sector_performance).json()
    sector_performance = pd.DataFrame.from_dict(sector_performance_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    sector_performance.to_csv("sector_performance", encoding='utf-8', index=False, sep=',')
    sector_performance_file = open("sector_performance")
    defaults = dict(
    market_date = market_date,
    sector_performance = File(sector_performance_file)
    )
    sector_performance, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_upcoming_earnings():
    url_upcoming_earnings = 'https://financialmodelingprep.com/api/v3/earning_calendar?apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    upcoming_earnings_json = requests.get(url_upcoming_earnings).json()
    upcoming_earnings = pd.DataFrame.from_dict(upcoming_earnings_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    upcoming_earnings.to_csv("upcoming_earnings", encoding='utf-8', index=False, sep=',')
    upcoming_earnings_file = open("upcoming_earnings")
    defaults = dict(
    market_date = market_date,
    upcoming_earnings = File(upcoming_earnings_file)
    )
    upcoming_earnings, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")

def get_new_ipo():
    url_new_ipo = 'https://financialmodelingprep.com/api/v3/ipo_calendar?&apikey=4ea5593093f3202bae9ca992c7ff4ce6'
    new_ipo_json = requests.get(url_new_ipo).json()
    new_ipo = pd.DataFrame.from_dict(new_ipo_json)
    market_datetime = datetime.datetime.now()
    market_date = market_datetime.strftime("%Y-%m-%d")
    new_ipo.to_csv("new_ipo", encoding='utf-8', index=False, sep=',')
    new_ipo_file = open("new_ipo")
    defaults = dict(
    market_date = market_date,
    new_ipo = File(new_ipo_file)
    )
    new_ipo, _ = Market.objects.update_or_create(defaults=defaults, market_date = market_date)
    return HttpResponseRedirect("/stocks/markets/")
