from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files import File
from .models import Stock, Market
from users.forms import PortfolioCreateForm
from .forms import StockSearchForm, AddToPortfolioFormSet, AddToPortfolio
import requests
import pandas as pd
import xmltodict
from django.views.generic import View
from .apicalls import get_major_indexes, get_most_active, get_top_gainers, get_top_losers, get_sector_performance, get_upcoming_earnings, get_new_ipo
from users.models import Portfolio
from django.forms import modelformset_factory
from django.contrib.auth.models import User

pd.set_option('display.max_colwidth', None)

class HomePageView(TemplateView):
    template_name = "Securities/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        return context

class MarketsView(TemplateView):
    template_name = "Securities/markets.html"
    model = Market

    def get_context_data(self, *args, **kwargs):
        context = {
            'stock_search_form': StockSearchForm(),
            'indexes_data': get_major_indexes(),
            'most_active': get_most_active(),
            'top_gainers_data': get_top_gainers(),
            'top_losers_data': get_top_losers(),
            'sector_performance_data': get_sector_performance(),
            'upcoming_earnings_data':get_upcoming_earnings(),
            'new_ipo_data': get_new_ipo(),
            'markets_data': Market.objects.all()
        }
        return context

class StockCreateView(CreateView):
    model = Stock
    fields = ['symbol']
    def form_valid(self, form):
        symbol = form.cleaned_data['symbol'].upper()
        url_quote = 'API'
        url_profile = 'API'
        url_rating = 'API'
        url_historical_timeseries = 'API'
        url_quarterly_income_stmt = 'API'
        url_annual_income_stmt = 'API'
        url_dividend_history_timeseries = 'API'
        url_key_executives = 'API'

        url_quarterly_balance_sheet_stmt = 'API'
        url_annual_balance_sheet_stmt = 'API'

        url_quarterly_cash_flow_stmt = 'API'
        url_annual_cash_flow_stmt = 'API'

        url_quarterly_financial_growth_stmt = 'API'
        url_annual_financial_growth_stmt = 'API'

        url_quarterly_financial_ratio_stmt = 'API'
        url_annual_financial_ratio_stmt = 'API'

        url_quarterly_enterprise_value_stmt = 'API'
        url_annual_enterprise_value_stmt = 'API'

        url_quarterly_key_metrics_stmt = 'API'
        url_annual_key_metrics_stmt = 'API'

        historical_dividend_json = requests.get(url_dividend_history_timeseries.format(symbol)).json()
        historical_dividend_date_dividend_col = pd.DataFrame({'date': ['a'], 'B': ['b']})
        try:
            historical_dividend = pd.DataFrame.from_dict(historical_dividend_json['historical'])
            historical_dividend_date_dividend_col = historical_dividend[['date', 'adjDividend']]
        except KeyError:
            "NO DIVIDEND DATA"

        historical_timeseries_json = requests.get(url_historical_timeseries.format(symbol)).json()
        historical_timeseries = pd.DataFrame.from_dict(historical_timeseries_json['historical'])
        historical_timeseries.to_csv(symbol+"_historical_timeseries", encoding='utf-8', index=False, sep=',')
        historical_timeseries_file = open(symbol+"_historical_timeseries")

        historical_timeseries_json = requests.get(url_historical_timeseries.format(symbol)).json()
        historical_timeseries = pd.DataFrame.from_dict(historical_timeseries_json['historical']).merge(historical_dividend_date_dividend_col, on = 'date', how ='outer')
        historical_timeseries.to_csv(symbol+"_historical_timeseries", encoding='utf-8', index=False, sep=',')
        historical_timeseries_file = open(symbol+"_historical_timeseries")

        key_executives_json = requests.get(url_key_executives.format(symbol)).json()
        key_executives = pd.DataFrame.from_dict(key_executives_json)
        key_executives.to_csv(symbol+"_key_executives", encoding='utf-8', index=False, sep=',')
        key_executives_file = open(symbol+"_key_executives")

        quarterly_income_stmt_json = requests.get(url_quarterly_income_stmt.format(symbol)).json()
        quarterly_income_stmt = pd.DataFrame.from_dict(quarterly_income_stmt_json)
        quarterly_income_stmt.to_csv(symbol+"_quarterly_income_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_income_stmt_file = open(symbol+"_quarterly_income_stmt")

        annual_income_stmt_json = requests.get(url_annual_income_stmt.format(symbol)).json()
        annual_income_stmt = pd.DataFrame.from_dict(annual_income_stmt_json)
        annual_income_stmt.to_csv(symbol+"_annual_income_stmt", encoding='utf-8', index=False, sep=',')
        annual_income_stmt_file = open(symbol+"_annual_income_stmt")

        quarterly_balance_sheet_stmt_json = requests.get(url_quarterly_balance_sheet_stmt.format(symbol)).json()
        quarterly_balance_sheet_stmt = pd.DataFrame.from_dict(quarterly_balance_sheet_stmt_json)
        quarterly_balance_sheet_stmt.to_csv(symbol+"_quarterly_balance_sheet_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_balance_sheet_stmt_file = open(symbol+"_quarterly_balance_sheet_stmt")

        annual_balance_sheet_stmt_json = requests.get(url_annual_balance_sheet_stmt.format(symbol)).json()
        annual_balance_sheet_stmt = pd.DataFrame.from_dict(annual_balance_sheet_stmt_json)
        annual_balance_sheet_stmt.to_csv(symbol+"_annual_balance_sheet_stmt", encoding='utf-8', index=False, sep=',')
        annual_balance_sheet_stmt_file = open(symbol+"_annual_balance_sheet_stmt")

        quarterly_cash_flow_stmt_json = requests.get(url_quarterly_cash_flow_stmt.format(symbol)).json()
        quarterly_cash_flow_stmt = pd.DataFrame.from_dict(quarterly_cash_flow_stmt_json)
        quarterly_cash_flow_stmt.to_csv(symbol+"_quarterly_cash_flow_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_cash_flow_stmt_file = open(symbol+"_quarterly_cash_flow_stmt")

        annual_cash_flow_stmt_json = requests.get(url_annual_cash_flow_stmt.format(symbol)).json()
        annual_cash_flow_stmt = pd.DataFrame.from_dict(annual_cash_flow_stmt_json)
        annual_cash_flow_stmt.to_csv(symbol+"_annual_cash_flow_stmt", encoding='utf-8', index=False, sep=',')
        annual_cash_flow_stmt_file = open(symbol+"_annual_cash_flow_stmt")

        quarterly_financial_growth_stmt_json = requests.get(url_quarterly_financial_growth_stmt.format(symbol)).json()
        quarterly_financial_growth_stmt = pd.DataFrame.from_dict(quarterly_financial_growth_stmt_json)
        quarterly_financial_growth_stmt.to_csv(symbol+"_quarterly_financial_growth_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_financial_growth_stmt_file = open(symbol+"_quarterly_financial_growth_stmt")

        annual_financial_growth_stmt_json = requests.get(url_annual_financial_growth_stmt.format(symbol)).json()
        annual_financial_growth_stmt = pd.DataFrame.from_dict(annual_financial_growth_stmt_json)
        annual_financial_growth_stmt.to_csv(symbol+"_annual_financial_growth_stmt", encoding='utf-8', index=False, sep=',')
        annual_financial_growth_stmt_file = open(symbol+"_annual_financial_growth_stmt")

        quarterly_financial_ratio_stmt_json = requests.get(url_quarterly_financial_ratio_stmt.format(symbol)).json()
        quarterly_financial_ratio_stmt = pd.DataFrame.from_dict(quarterly_financial_ratio_stmt_json)
        quarterly_financial_ratio_stmt.to_csv(symbol+"_quarterly_financial_ratio_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_financial_ratio_stmt_file = open(symbol+"_quarterly_financial_ratio_stmt")

        annual_financial_ratio_stmt_json = requests.get(url_annual_financial_ratio_stmt.format(symbol)).json()
        annual_financial_ratio_stmt = pd.DataFrame.from_dict(annual_financial_ratio_stmt_json)
        annual_financial_ratio_stmt.to_csv(symbol+"_annual_financial_ratio_stmt", encoding='utf-8', index=False, sep=',')
        annual_financial_ratio_stmt_file = open(symbol+"_annual_financial_ratio_stmt")

        quarterly_enterprise_value_stmt_json = requests.get(url_quarterly_enterprise_value_stmt.format(symbol)).json()
        quarterly_enterprise_value_stmt = pd.DataFrame.from_dict(quarterly_enterprise_value_stmt_json)
        quarterly_enterprise_value_stmt.to_csv(symbol+"_quarterly_enterprise_value_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_enterprise_value_stmt_file = open(symbol+"_quarterly_enterprise_value_stmt")

        annual_enterprise_value_stmt_json = requests.get(url_annual_enterprise_value_stmt.format(symbol)).json()
        annual_enterprise_value_stmt = pd.DataFrame.from_dict(annual_enterprise_value_stmt_json)
        annual_enterprise_value_stmt.to_csv(symbol+"_annual_enterprise_value_stmt", encoding='utf-8', index=False, sep=',')
        annual_enterprise_value_stmt_file = open(symbol+"_annual_enterprise_value_stmt")

        quarterly_key_metrics_stmt_json = requests.get(url_quarterly_key_metrics_stmt.format(symbol)).json()
        quarterly_key_metrics_stmt = pd.DataFrame.from_dict(quarterly_key_metrics_stmt_json)
        quarterly_key_metrics_stmt.to_csv(symbol+"_quarterly_key_metrics_stmt", encoding='utf-8', index=False, sep=',')
        quarterly_key_metrics_stmt_file = open(symbol+"_quarterly_key_metrics_stmt")

        annual_key_metrics_stmt_json = requests.get(url_annual_key_metrics_stmt.format(symbol)).json()
        annual_key_metrics_stmt = pd.DataFrame.from_dict(annual_key_metrics_stmt_json)
        annual_key_metrics_stmt.to_csv(symbol+"_annual_key_metrics_stmt", encoding='utf-8', index=False, sep=',')
        annual_key_metrics_stmt_file = open(symbol+"_annual_key_metrics_stmt")

        quote_json = requests.get(url_quote.format(symbol)).json()
        quote = pd.DataFrame(quote_json, index = [0])
        profile_json = requests.get(url_profile.format(symbol)).json()
        profile = pd.DataFrame(profile_json, index = [0])
        rating_json = requests.get(url_rating.format(symbol)).json()
        rating = pd.DataFrame(rating_json, index = [0])

        url_news_description = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s={}'
        xml_data = requests.get(url_news_description.format(symbol))
        parse_data = xmltodict.parse(xml_data.text)
        json_news_data = parse_data['rss']['channel']['item']
        list_news = []
        for items in json_news_data:
            text = items['guid']['#text']
            append_text = text[:0] + 'ninektechnologies' + text[0:]
            title = items['title']
            description = items['description']
            pub_date = items['pubDate']
            link = items['link']
            news_data_dict = {
                'text': append_text,
                'title': title,
                'description': description,
                'pub_date': pub_date,
                'link': link,
            }
            list_news.append(news_data_dict)
        yahoonews = list_news

        if len(quote_json) != 0:
            name = quote['name'].to_string(header=None, index=None)
            price = quote['price'].to_string(header=None, index=None)
            dayLow = quote['dayLow'].to_string(header=None, index=None)
            dayHigh = quote['dayHigh'].to_string(header=None, index=None)
            yearHigh = quote['yearHigh'].to_string(header=None, index=None)
            yearLow = quote['yearLow'].to_string(header=None, index=None)
            priceAvg50 = quote['priceAvg50'].to_string(header=None, index=None)
            priceAvg200 = quote['priceAvg200'].to_string(header=None, index=None)
            volume = quote['volume'].to_string(header=None, index=None)
            avgVolume = quote['avgVolume'].to_string(header=None, index=None)
            openPrice = quote['open'].to_string(header=None, index=None)
            previousClose = quote['previousClose'].to_string(header=None, index=None)
            eps = quote['eps'].to_string(header=None, index=None)
            earningsAnnouncement = quote['earningsAnnouncement'].to_string(header=None, index=None)
            sharesOutstanding = quote['sharesOutstanding'].to_string(header=None, index=None)
        else:
            name = "—"
            price = "—"
            dayLow = "—"
            dayHigh = "—"
            yearHigh = "—"
            yearLow = "—"
            priceAvg50 = "—"
            priceAvg200 = "—"
            volume = "—"
            avgVolume = "—"
            openPrice = "—"
            previousClose = "—"
            eps = "—"
            earningsAnnouncement = "—"
            sharesOutstanding = "—" #END QUOTE

        if len(profile_json) != 0:
            beta = profile['beta'].to_string(header=None, index=None)
            last_Div = profile['lastDiv'].to_string(header=None, index=None)
            exchange = profile['exchange'].to_string(header=None, index=None)
            exchangeShortName = profile['exchangeShortName'].to_string(header=None, index=None)
            industry = profile['industry'].to_string(header=None, index=None)
            website = profile['website'].to_string(header=None, index=None)
            description = profile['description'].to_string(header=None, index=None)
            ceo = profile['ceo'].to_string(header=None, index=None)
            sector = profile['sector'].to_string(header=None, index=None)
            country = profile['country'].to_string(header=None, index=None)
            fullTimeEmployees = profile['fullTimeEmployees'].to_string(header=None, index=None)
            phone = profile['phone'].to_string(header=None, index=None)
            address = profile['address'].to_string(header=None, index=None)
            city = profile['city'].to_string(header=None, index=None)
            state = profile['state'].to_string(header=None, index=None)
            zip = profile['zip'].to_string(header=None, index=None)
            dcfDiff = profile['dcfDiff'].to_string(header=None, index=None)
            dcf =  profile['dcf'].to_string(header=None, index=None)
            stock_logo =  profile['image'].to_string(header=None, index=None)
        else:
            beta = "—"
            last_Div = "—"
            exchange = "—"
            exchangeShortName = "—"
            industry = "—"
            website = "—"
            description = "—"
            ceo = "—"
            sector = "—"
            country = "—"
            fullTimeEmployees = "—"
            phone = "—"
            address = "—"
            city = "—"
            state = "—"
            zip = "—"
            dcfDiff = "—"
            dcf = "—"
            stock_logo = "—"  #End Profile

        if len(rating_json) != 0:
            rating_date = rating['date'].to_string(header=None, index=None)
            rating_alpha = rating['rating'].to_string(header=None, index=None)
            ratingScore = rating['ratingScore'].to_string(header=None, index=None)
            ratingRecommendation = rating['ratingRecommendation'].to_string(header=None, index=None)
            ratingDetailsDCFScore = rating['ratingDetailsDCFScore'].to_string(header=None, index=None)
            ratingDetailsDCFRecommendation = rating['ratingDetailsDCFRecommendation'].to_string(header=None, index=None)
            ratingDetailsROEScore = rating['ratingDetailsROEScore'].to_string(header=None, index=None)
            ratingDetailsROERecommendation = rating['ratingDetailsROERecommendation'].to_string(header=None, index=None)
            ratingDetailsROAScore = rating['ratingDetailsROAScore'].to_string(header=None, index=None)
            ratingDetailsROARecommendation = rating['ratingDetailsROARecommendation'].to_string(header=None, index=None)
            ratingDetailsDEScore = rating['ratingDetailsDEScore'].to_string(header=None, index=None)
            ratingDetailsDERecommendation = rating['ratingDetailsDERecommendation'].to_string(header=None, index=None)
            ratingDetailsPEScore = rating['ratingDetailsPEScore'].to_string(header=None, index=None)
            ratingDetailsPERecommendation = rating['ratingDetailsPERecommendation'].to_string(header=None, index=None)
            ratingDetailsPBScore = rating['ratingDetailsPBScore'].to_string(header=None, index=None)
            ratingDetailsPBRecommendation = rating['ratingDetailsPBRecommendation'].to_string(header=None, index=None)
        else:
            rating_date = '—'
            rating_alpha = '—'
            ratingScore = '—'
            ratingRecommendation = '—'
            ratingDetailsDCFScore = '—'
            ratingDetailsDCFRecommendation = '—'
            ratingDetailsROEScore = '—'
            ratingDetailsROERecommendation = '—'
            ratingDetailsROAScore = '—'
            ratingDetailsROARecommendation = '—'
            ratingDetailsDEScore = '—'
            ratingDetailsDERecommendation = '—'
            ratingDetailsPEScore = '—'
            ratingDetailsPERecommendation = '—'
            ratingDetailsPBScore = '—'
            ratingDetailsPBRecommendation = '—' #END RATING

        defaults = dict(
        yahoonews = yahoonews,
        historicalTimeseries = File(historical_timeseries_file),
        quarterly_income_statement = File(quarterly_income_stmt_file),
        annual_income_statement = File(annual_income_stmt_file),
        key_executives = File(key_executives_file),
        quarterly_balance_sheet_statement = File(quarterly_balance_sheet_stmt_file),
        annual_balance_sheet_statement = File(annual_balance_sheet_stmt_file),

        quarterly_cash_flow_statement = File(quarterly_cash_flow_stmt_file),
        annual_cash_flow_statement = File(annual_cash_flow_stmt_file),

        quarterly_financial_growth = File(quarterly_financial_growth_stmt_file),
        annual_financial_growth = File(annual_financial_growth_stmt_file),

        quarterly_financial_ratio = File(quarterly_financial_ratio_stmt_file),
        annual_financial_ratio = File(annual_financial_ratio_stmt_file),

        quarterly_enterprise_value = File(quarterly_enterprise_value_stmt_file),
        annual_enterprise_value = File(annual_enterprise_value_stmt_file),

        quarterly_key_metrics = File(quarterly_key_metrics_stmt_file),
        annual_key_metrics = File(annual_key_metrics_stmt_file),

        name=name,
        price = price,
        dayLow=dayLow,
        dayHigh = dayHigh,
        yearHigh=yearHigh,
        yearLow = yearLow,
        priceAvg50=priceAvg50,
        priceAvg200 = priceAvg200,
        volume=volume,
        avgVolume = avgVolume,
        openPrice=openPrice,
        previousClose = previousClose,
        eps=eps,
        sharesOutstanding = sharesOutstanding,
        earningsAnnouncement = earningsAnnouncement, #End Quote
        ratingDate = rating_date,
        rating = rating_alpha,
        ratingScore = ratingScore,
        ratingRecommendation = ratingRecommendation,
        ratingDetailsDCFScore = ratingDetailsDCFScore,
        ratingDetailsDCFRecommendation = ratingDetailsDCFRecommendation,
        ratingDetailsROEScore = ratingDetailsROEScore,
        ratingDetailsROERecommendation = ratingDetailsROERecommendation,
        ratingDetailsROAScore = ratingDetailsROAScore,
        ratingDetailsROARecommendation = ratingDetailsROARecommendation,
        ratingDetailsDEScore = ratingDetailsDEScore,
        ratingDetailsDERecommendation = ratingDetailsDERecommendation,
        ratingDetailsPEScore = ratingDetailsPEScore,
        ratingDetailsPERecommendation = ratingDetailsPERecommendation,
        ratingDetailsPBScore = ratingDetailsPBScore,
        ratingDetailsPBRecommendation = ratingDetailsPBRecommendation, #END RATING
        beta = beta,
        last_Div = last_Div,
        exchange = exchange,
        exchangeShortName = exchangeShortName,
        industry = industry,
        website = website,
        description = description,
        ceo = ceo,
        sector = sector,
        country = country,
        fullTimeEmployees = fullTimeEmployees,
        phone = phone,
        address = address,
        city = city,
        state = state,
        zip = zip,
        dcfDiff = dcfDiff,
        dcf = dcf,
        stock_logo = stock_logo) #End Profile

        ticker, _ = Stock.objects.update_or_create(defaults=defaults, symbol=symbol)
        # return HttpResponse(ticker.pk)
        return HttpResponseRedirect("/stocks/" + str(ticker.slug) + "/")

class StockListView(ListView):
    model = Stock
    template_name = 'securities/stock-most-popular.html'
    context_object_name = 'symbols'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()
        context['portfolio_create_form'] = PortfolioCreateForm()
        if self.request.user.is_active:
            context['portfolio_list'] = Portfolio.objects.filter(portfolio_author=self.request.user)
        return context

from django.shortcuts import get_object_or_404

class StockDetailView(DetailView):
    model = Stock
    template_name = 'securities/stock_detail.html'

    def post(self, request, slug, *args, **kwargs):
        add_to_portfolio = AddToPortfolioFormSet(request.POST)
        symbol = get_object_or_404(Stock, slug = self.kwargs['slug'])
        portfolio_queryset = Portfolio.objects.filter(portfolio_author = self.request.user)

        if request.method == 'POST':
            form_zero = 'form-0-portfolio_name'
            form_one = 'form-1-portfolio_name'
            form_two = 'form-2-portfolio_name'
            form_three = 'form-3-portfolio_name'
            form_four = 'form-4-portfolio_name'
            form_five = 'form-5-portfolio_name'

            if request.POST.get(form_zero):
                add_to_portfolio_from_zero = request.POST.get(form_zero)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_zero)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            if request.POST.get(form_one):
                add_to_portfolio_from_one = request.POST.get(form_one)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_one)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            if request.POST.get(form_two):
                add_to_portfolio_from_two = request.POST.get(form_two)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_two)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            if request.POST.get(form_three):
                add_to_portfolio_from_three = request.POST.get(form_three)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_three)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            if request.POST.get(form_four):
                add_to_portfolio_from_four = request.POST.get(form_four)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_four)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            if request.POST.get(form_five):
                add_to_portfolio_from_five = request.POST.get(form_five)
                name = portfolio_queryset.get(portfolio_name = add_to_portfolio_from_five)
                if name.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                    name.portfolio_symbols.remove(symbol)
                else:
                    name.portfolio_symbols.add(symbol)

            return HttpResponseRedirect("/stocks/" + self.kwargs['slug'] + "/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_search_form'] = StockSearchForm()

        symbol = get_object_or_404(Stock, slug = self.kwargs['slug'])
        is_watching = False
        add_remove_action_list = []
        portfolio_queryset = Portfolio.objects.filter(portfolio_author = self.request.user)
        for portfolio in portfolio_queryset:
            if portfolio.portfolio_symbols.filter(slug=self.kwargs['slug']).exists():
                is_watching = True
                action = "REMOVE"
            else:
                action = "ADD"
            add_remove_action_list.append(action)
        context['is_watching'] = is_watching
        context['add_remove_action_list'] = add_remove_action_list

        if self.request.user.is_active:
            context['add_to_portfolio'] = AddToPortfolioFormSet(queryset = Portfolio.objects.filter(portfolio_author=self.request.user)) #Pass queryset here
        if self.request.user.is_active:
            context['portfolio_list'] = Portfolio.objects.filter(portfolio_author=self.request.user)
        return context
