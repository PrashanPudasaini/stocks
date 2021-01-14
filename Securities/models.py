from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import pandas as pd
from Securities.storage import OverwriteStorage
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
import string
from django.utils.text import slugify
import random
from django.urls import reverse


class Market(models.Model):
    market_date = models.CharField(max_length = 60, blank = False, default = "")
    most_active = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_most_active', blank = True, null = True)
    top_gainers = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_top_gainers', blank = True, null = True)
    top_losers = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_top_losers', blank = True, null = True)
    sector_performance = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_sector_performance', blank = True, null = True)
    major_indexes = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_major_indexes', blank = True, null = True)
    upcoming_earnings = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='makets_upcoming_earnings', blank = True, null = True)
    new_ipo = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_new_ipo', blank = True, null = True)
    latest_news = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='markets_news', blank = True, null = True)

    def __str__(self):
        return self.market_date

    def display_major_indexes(self):
        columns = ['SYMBOL', 'NAME', 'PRICE', 'CHANGE %', 'CHANGE', 'DAY LOW', 'DAY HIGH', 'YEAR HIGH', 'YEAR LOW', 'MARKET CAP', 'PRICE AVG 50', 'PRICE AVG 200', 'VOLUME', 'AVG VOL', 'EXCHANGE', 'OPEN', 'PREVIOUS CLOSE', 'EPS', 'PE', 'EARNINGS ANNOUNCEMENT', 'SHARES OUTS', 'TIME STAMP']
        df = pd.read_csv(self.major_indexes.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,10,11,12,13,15,16]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_most_active(self):
        columns = ['SYMBOL', 'CHANGE', 'PRICE', 'CHANGE %', 'NAME']
        df = pd.read_csv(self.most_active.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_top_gainers(self):
        columns = ['SYMBOL', 'CHANGE', 'PRICE', 'CHANGE %', 'NAME']
        df = pd.read_csv(self.top_gainers.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_top_losers(self):
        columns = ['SYMBOL', 'CHANGE', 'PRICE', 'CHANGE %', 'NAME']
        df = pd.read_csv(self.top_losers.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_sector_performance(self):
        columns = ['SECTOR', 'CHANGE PERCENTAGE']
        df = pd.read_csv(self.sector_performance.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_upcoming_earnings(self):
        columns = ['DATE', 'SYMBOL', 'EPS', 'EPS ESTIMATE', 'TIME', 'REVENUE', 'REVENUE ESTIMATE']
        df = pd.read_csv(self.upcoming_earnings.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,5,6]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

    def display_new_ipo(self):
        columns = ['DATE', 'COMPANY', 'SYMBOL', 'EXCHANGE', 'ACTIONS', 'SHARES', 'PRICE', 'MARKET CAP']
        df = pd.read_csv(self.new_ipo.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=False, border=1, index=False, index_names=False, header=True)
            return data_table

class Stock(models.Model):
    symbol = models.CharField(max_length = 10, blank = False, default = "")
    date_created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    yahoonews = JSONField(blank = True, null = True)
    name = models.CharField(max_length = 500, blank = True, default = "")
    price = models.CharField(max_length = 500, blank = True, default = "")
    dayLow = models.CharField(max_length = 500, blank = True, default = "")
    dayHigh = models.CharField(max_length = 500, blank = True, default = "")
    yearHigh = models.CharField(max_length = 500, blank = True, default = "")
    yearLow = models.CharField(max_length = 500, blank = True, default = "")
    priceAvg50 = models.CharField(max_length = 500, blank = True, default = "")
    priceAvg200 = models.CharField(max_length = 500, blank = True, default = "")
    volume = models.CharField(max_length = 500, blank = True, default = "")
    avgVolume = models.CharField(max_length = 500, blank = True, default = "")
    openPrice = models.CharField(max_length = 500, blank = True, default = "")
    previousClose = models.CharField(max_length = 500, blank = True, default = "")
    eps = models.CharField(max_length = 500, blank = True, default = "")
    earningsAnnouncement = models.CharField(max_length = 500, blank = True, default = "")
    sharesOutstanding = models.CharField(max_length = 500, blank = True, default = "") #End Quote

    beta = models.CharField(max_length = 500, blank = True, default = "")
    last_Div = models.CharField(max_length = 500, blank = True, default = "")
    exchange = models.CharField(max_length = 500, blank = True, default = "")
    exchangeShortName = models.CharField(max_length = 500, blank = True, default = "")
    industry = models.CharField(max_length = 500, blank = True, default = "")
    website = models.URLField(default = "", null = True, blank = True)
    description = models.TextField(blank = True, default = "")
    ceo = models.CharField(max_length = 500, blank = True, default = "")
    sector = models.CharField(max_length = 500, blank = True, default = "")
    country = models.CharField(max_length = 500, blank = True, default = "")
    fullTimeEmployees = models.CharField(max_length = 500, blank = True, default = "")
    phone = models.CharField(max_length = 500, blank = True, default = "")
    address = models.CharField(max_length = 500, blank = True, default = "")
    city = models.CharField(max_length = 500, blank = True, default = "")
    state = models.CharField(max_length = 500, blank = True, default = "")
    zip = models.CharField(max_length = 500, blank = True, default = "")
    dcfDiff = models.CharField(max_length = 500, blank = True, default = "")
    dcf = models.CharField(max_length = 500, blank = True, default = "")

    ratingDate = models.CharField(max_length = 500, blank = True, default = "")
    rating = models.CharField(max_length = 500, blank = True, default = "")
    ratingScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingRecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsDCFScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsDCFRecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsROEScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsROERecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsROAScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsROARecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsDEScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsDERecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsPEScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsPERecommendation = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsPBScore = models.CharField(max_length = 500, blank = True, default = "")
    ratingDetailsPBRecommendation = models.CharField(max_length = 500, blank = True, default = "")

    key_executives = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='stock_detail_key_executives', blank = True, null = True)

    stock_logo = models.ImageField(max_length=500, storage=OverwriteStorage(), upload_to = 'stocks_logo', null = True, blank = True)
    historicalTimeseries = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='historical_timeseries', blank = True, null = True)

    quarterly_income_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_income_stmt', blank = True, null = True)
    annual_income_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_income_stmt', blank = True, null = True)

    quarterly_balance_sheet_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_balance_sheet_stmt', blank = True, null = True)
    annual_balance_sheet_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_balance_sheet_stmt', blank = True, null = True)

    quarterly_cash_flow_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_cash_flow_stmt', blank = True, null = True)
    annual_cash_flow_statement = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_cash_flow_stmt', blank = True, null = True)

    quarterly_financial_growth = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_financial_growth', blank = True, null = True)
    annual_financial_growth = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_financial_growth', blank = True, null = True)

    quarterly_financial_ratio = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_financial_ratio', blank = True, null = True)
    annual_financial_ratio = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_financial_ratio', blank = True, null = True)

    quarterly_enterprise_value = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_enterprise_value', blank = True, null = True)
    annual_enterprise_value = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_enterprise_value', blank = True, null = True)

    quarterly_key_metrics = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='quarterly_key_metrics', blank = True, null = True)
    annual_key_metrics = models.FileField(max_length=500, storage=OverwriteStorage(), upload_to='annual_key_metrics', blank = True, null = True)

    def __str__(self):
        return self.symbol


#-------------------------FINANCIALS - NET INCOME CHART-----------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    # def chart_annual_net_income(self):
    #     col_list = ["netIncome", "period"]
    #     df = pd.read_csv(self.annual_income_statement.path, usecols=col_list, nrows = 4)
    #     to_array_of_objects = df.to_dict('records')
    #
    #     if len(to_array_of_objects) == 0:
    #         return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
    #     else:
    #         return to_array_of_objects

#-------------------------KEY EXECUTIVES DATATABLE------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def display_key_executives(self):
        columns = ['Title', 'Name', 'Pay', 'Pay Currency', 'Gender', 'Year Born', 'Title Since']
        df = pd.read_csv(self.key_executives.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

#-------------------------HISTORICAL TIMESERIES DATAFRAME-----------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def display_historical_timeseries_2d(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=2)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_last_five_days(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=5)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_1m(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=22)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_3m(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=66)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_6m(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=132)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_1y(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=264)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_3y(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=792)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_5y(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Unadjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            last_n_days_data = df_hide_first_row.head(n=1320)
            data_table = last_n_days_data.to_html(na_rep = '—', show_dimensions=True, border=1, index=True, index_names=False, header=True)
            return data_table

    def display_historical_timeseries_max(self):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'UnAdjusted Volume', 'Change', 'Change %', 'VWAP', 'Label', 'Change Over Time','Dividend', 'Split']
        df = pd.read_csv(self.historicalTimeseries.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,1,2,3,4,5,6,7,8,9,10,12,13,14]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_income_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Revenue', 'Cost of Revenue', 'Gross Profit', 'Gross Profit Ratio', 'R&D Expenses', 'G&A Expense', 'S&M Expense', 'Other Expenses', 'Operating Expenses', 'Cost and Expense', 'Interest Expense', 'D&A', 'EBITDA', 'EBITDA Ratio', 'Operating Income', 'Operating Income Ratio', 'Total Other Income Expenses (Net)', 'Income Before Tax', 'Income Before Tax Ratio', 'Income Tax Expense', 'Net Income', 'Net Income Ratio', 'EPS', 'EPS Diluted', 'Weighted Avg. SHS Out', 'Weighted Avg. SHS Out Diluted', 'Link', 'Final Link']
        df = pd.read_csv(self.quarterly_income_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_income_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Revenue', 'Cost of Revenue', 'Gross Profit', 'Gross Profit Ratio', 'R&D Expenses', 'G&A Expense', 'S&M Expense', 'Other Expenses', 'Operating Expenses', 'Cost and Expense', 'Interest Expense', 'D&A', 'EBITDA', 'EBITDA Ratio', 'Operating Income', 'Operating Income Ratio', 'Total Other Income Expenses (Net)', 'Income Before Tax', 'Income Before Tax Ratio', 'Income Tax Expense', 'Net Income', 'Net Income Ratio', 'EPS', 'EPS Diluted', 'Weighted Avg. SHS Out', 'Weighted Avg. SHS Out Diluted', 'Link', 'Final Link']
        df = pd.read_csv(self.annual_income_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_balance_sheet_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Cash And Cash Equivalents', 'Short Term Investments', 'Cash And Short Term Investments', 'Net Receivables', 'Inventory', 'Other Current Assets', 'Total Current Assets', 'Property Plant EquipmentNet', 'Goodwill', 'Intangible Assets', 'Goodwill And Intangible Assets', 'Long Term Investments', 'Tax Assets', 'Other Non Current Assets', 'Total Non Current Assets', 'Other Assets', 'Total Assets', 'Account Payables', 'Short Term Debt', 'Tax Payables', 'Deferred Revenue', 'Other Current Liabilities', 'Total Current Liabilities', 'Long Term Debt', 'Deferred Revenue Non Current', 'Deferred Tax Liabilities Non Current', 'Other Non Current Liabilities', 'Total Non Current Liabilities', 'Other Liabilities', 'Total Liabilities', 'Common Stock', 'Retained Earnings', 'Accumulated Other Comprehensive Income Loss', 'Other Total Stockholders Equity', 'Total Stockholders Equity', 'Total Liabilities And Stockholders Equity', 'Total Investments', 'Total Debt', 'Net Debt', 'Link', 'Final Link']
        df = pd.read_csv(self.quarterly_balance_sheet_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_balance_sheet_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Cash And Cash Equivalents', 'Short Term Investments', 'Cash And Short Term Investments', 'Net Receivables', 'Inventory', 'Other Current Assets', 'Total Current Assets', 'Property Plant EquipmentNet', 'Goodwill', 'Intangible Assets', 'Goodwill And Intangible Assets', 'Long Term Investments', 'Tax Assets', 'Other Non Current Assets', 'Total Non Current Assets', 'Other Assets', 'Total Assets', 'Account Payables', 'Short Term Debt', 'Tax Payables', 'Deferred Revenue', 'Other Current Liabilities', 'Total Current Liabilities', 'Long Term Debt', 'Deferred Revenue Non Current', 'Deferred Tax Liabilities Non Current', 'Other Non Current Liabilities', 'Total Non Current Liabilities', 'Other Liabilities', 'Total Liabilities', 'Common Stock', 'Retained Earnings', 'Accumulated Other Comprehensive Income Loss', 'Other Total Stockholders Equity', 'Total Stockholders Equity', 'Total Liabilities And Stockholders Equity', 'Total Investments', 'Total Debt', 'Net Debt', 'Link', 'Final Link']
        df = pd.read_csv(self.annual_balance_sheet_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_cash_flow_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Net Income', 'D&A', 'Deferred Income Tax', 'Stock Based Compensation', 'Change In Working Capital', 'Accounts Receivables', 'Inventory', 'Accounts Payables', 'Other Working Capital', 'Other Non Cash Items', 'Net Cash Provided By Operating Activities', 'Investments In Property Plant And Equipment', 'Acquisitions Net', 'Purchases Of Investments', 'Sales Maturities Of Investments', 'Other Investing Activites', 'Net Cash Used For Investing Activites', 'Debt Repayment', 'Common Stock Issued', 'Common Stock Repurchased', 'Dividends Paid', 'Other Financing Activites', 'Net Cash Used Provided By Financing Activities', 'Effect Of Forex Changes On Cash', 'Net Change In Cash', 'Cash At End Of Period', 'Cash At Beginning Of Period', 'Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow', 'Link', 'Final Link']
        df = pd.read_csv(self.quarterly_cash_flow_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_cash_flow_statement(self):
        columns = ['Date', 'Symbol', 'Filling Date', 'Accepted Date', 'Period', 'Net Income', 'D&A', 'Deferred Income Tax', 'Stock Based Compensation', 'Change In Working Capital', 'Accounts Receivables', 'Inventory', 'Accounts Payables', 'Other Working Capital', 'Other Non Cash Items', 'Net Cash Provided By Operating Activities', 'Investments In Property Plant And Equipment', 'Acquisitions Net', 'Purchases Of Investments', 'Sales Maturities Of Investments', 'Other Investing Activites', 'Net Cash Used For Investing Activites', 'Debt Repayment', 'Common Stock Issued', 'Common Stock Repurchased', 'Dividends Paid', 'Other Financing Activites', 'Net Cash Used Provided By Financing Activities', 'Effect Of Forex Changes On Cash', 'Net Change In Cash', 'Cash At End Of Period', 'Cash At Beginning Of Period', 'Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow', 'Link', 'Final Link']
        df = pd.read_csv(self.annual_cash_flow_statement.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, render_links = True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_financial_growth_statement(self):
        columns = ['Symbol', 'Date', 'Revenue Growth', 'Gross Profit Growth', 'EBIT Growth', 'Operating Income Growth', 'Net Income Growth', 'EPS Growth', 'EPS Diluted Growth', 'Weighted Average Shares Growth', 'Weighted Average Shares Diluted Growth', 'Dividends Per Share Growth', 'Operating Cash Flow Growth', 'Free Cash Flow Growth', 'Ten Years Revenue Growth Per Share', 'Five Years Revenue Growth Per Share', 'Three Years Revenue Growth Per Share', 'Ten Years Operating Cash Flow Growth Per Share', 'Five Years Operating Cash Flow Growth Per Share', 'Three Years Operating Cash Flow Growth Per Share', 'Ten Years Net Income Growth Per Share', 'Five Years Net Income Growth Per Share', 'Three Years Net Income Growth Per Share', 'Ten Years Shareholders Equity Growth Per Share', 'Five Years Shareholders Equity Growth Per Share', 'Three Years Shareholders Equity Growth Per Share', 'Ten Years Dividend Per Share Growth Per Share', 'Five Years Dividend Per Share Growth Per Share', 'Three Years Dividend Per Share Growth Per Share', 'Receivables Growth', 'Inventory Growth', 'Asset Growth', 'BVPS Growth', 'Debt Growth', 'R&D Expense Growth', 'SG&A Expenses Growth']
        df = pd.read_csv(self.quarterly_financial_growth.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_financial_growth_statement(self):
        columns = ['Symbol', 'Date', 'Revenue Growth', 'Gross Profit Growth', 'EBIT Growth', 'Operating Income Growth', 'Net Income Growth', 'EPS Growth', 'EPS Diluted Growth', 'Weighted Average Shares Growth', 'Weighted Average Shares Diluted Growth', 'Dividends Per Share Growth', 'Operating Cash Flow Growth', 'Free Cash Flow Growth', 'Ten Years Revenue Growth Per Share', 'Five Years Revenue Growth Per Share', 'Three Years Revenue Growth Per Share', 'Ten Years Operating Cash Flow Growth Per Share', 'Five Years Operating Cash Flow Growth Per Share', 'Three Years Operating Cash Flow Growth Per Share', 'Ten Years Net Income Growth Per Share', 'Five Years Net Income Growth Per Share', 'Three Years Net Income Growth Per Share', 'Ten Years Shareholders Equity Growth Per Share', 'Five Years Shareholders Equity Growth Per Share', 'Three Years Shareholders Equity Growth Per Share', 'Ten Years Dividend Per Share Growth Per Share', 'Five Years Dividend Per Share Growth Per Share', 'Three Years Dividend Per Share Growth Per Share', 'Receivables Growth', 'Inventory Growth', 'Asset Growth', 'BVPS Growth', 'Debt Growth', 'R&D Expense Growth', 'SG&A Expenses Growth']
        df = pd.read_csv(self.annual_financial_growth.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_financial_ratio_statement(self):
        columns = ['Symbol', 'Date', 'Current Ratio', 'Quick Ratio', 'Cash Ratio', 'Days Of Sales Outstanding', 'Days Of Inventory Outstanding', 'Operating Cycle', 'Days Of Payables Outstanding', 'Cash Conversion Cycle', 'Gross Profit Margin', 'Operating Profit Margin', 'Pre Tax Profit Margin', 'Net Profit Margin', 'Effective Tax Rate', 'Return On Assets', 'Return On Equity', 'Return On Capital Employed', 'Net Income Per EBT', 'EBT Per EBIT', 'EBIT Per Revenue', 'Debt Ratio', 'Debt Equity Ratio', 'Long Term Debt To Capitalization', 'Total Debt To Capitalization', 'Interest Coverage', 'Cash Flow To Debt Ratio', 'Company Equity Multiplier', 'Receivables Turnover', 'Payables Turnover', 'Inventory Turnover', 'Fixed Asset Turnover', 'Asset Turnover', 'Operating Cash Flow Per Share', 'Free Cash Flow Per Share', 'Cash Per Share', 'Payout Ratio', 'Operating Cash Flow Sales Ratio', 'Free Cash Flow Operating Cash Flow Ratio', 'Cash Flow Coverage Ratios', 'Short Term Coverage Ratios', 'Capital Expenditure Coverage Ratio', 'Dividend Paid And Capex Coverage Ratio', 'Dividend Payout Ratio', 'Price Book Value Ratio', 'Price To Book Ratio','Price To Sales Ratio', 'Price Earnings Ratio', 'Price To Free Cash Flow Ratio', 'Price To Operating Cash Flow Ratio', 'Price Cash Flow Ratio', 'Price Earnings To Growth Ratio', 'Price Sales Ratio', 'Dividend Yield', 'Enterprise Value Multiple', 'Price Fair Value']
        df = pd.read_csv(self.quarterly_financial_ratio.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_financial_ratio_statement(self):
        columns = ['Symbol', 'Date', 'Current Ratio', 'Quick Ratio', 'Cash Ratio', 'Days Of Sales Outstanding', 'Days Of Inventory Outstanding', 'Operating Cycle', 'Days Of Payables Outstanding', 'Cash Conversion Cycle', 'Gross Profit Margin', 'Operating Profit Margin', 'Pre Tax Profit Margin', 'Net Profit Margin', 'Effective Tax Rate', 'Return On Assets', 'Return On Equity', 'Return On Capital Employed', 'Net Income Per EBT', 'EBT Per EBIT', 'EBIT Per Revenue', 'Debt Ratio', 'Debt Equity Ratio', 'Long Term Debt To Capitalization', 'Total Debt To Capitalization', 'Interest Coverage', 'Cash Flow To Debt Ratio', 'Company Equity Multiplier', 'Receivables Turnover', 'Payables Turnover', 'Inventory Turnover', 'Fixed Asset Turnover', 'Asset Turnover', 'Operating Cash Flow Per Share', 'Free Cash Flow Per Share', 'Cash Per Share', 'Payout Ratio', 'Operating Cash Flow Sales Ratio', 'Free Cash Flow Operating Cash Flow Ratio', 'Cash Flow Coverage Ratios', 'Short Term Coverage Ratios', 'Capital Expenditure Coverage Ratio', 'Dividend Paid And Capex Coverage Ratio', 'Dividend Payout Ratio', 'Price Book Value Ratio', 'Price To Book Ratio','Price To Sales Ratio', 'Price Earnings Ratio', 'Price To Free Cash Flow Ratio', 'Price To Operating Cash Flow Ratio', 'Price Cash Flow Ratio', 'Price Earnings To Growth Ratio', 'Price Sales Ratio', 'Dividend Yield', 'Enterprise Value Multiple', 'Price Fair Value']
        df = pd.read_csv(self.annual_financial_ratio.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_enterprise_value_statement(self):
        columns = ['Symbol', 'Date', 'Stock Price', 'Number Of Shares', 'Market Capitalization', 'Cash And Cash Equivalents', 'Total Debt', 'Enterprise Value']
        df = pd.read_csv(self.quarterly_enterprise_value.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_enterprise_value_statement(self):
        columns = ['Symbol', 'Date', 'Stock Price', 'Number Of Shares', 'Market Capitalization', 'Cash And Cash Equivalents', 'Total Debt', 'Enterprise Value']
        df = pd.read_csv(self.annual_enterprise_value.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_quarterly_key_metrics_statement(self):
        columns = ['Symbol', 'Date', 'Revenue Per Share', 'Net Income Per Share', 'Operating Cash Flow Per Share', 'Free Cash Flow Per Share', 'Cash Per Share', 'Book Value Per Share', 'Tangible Book Value Per Share', 'Shareholders Equity Per Share', 'Interest Debt Per Share', 'Market Cap', 'Enterprise Value', 'PE Ratio', 'Price To Sales Ratio', 'POCF Ratio', 'PFCF Ratio', 'PB Ratio', 'PTB Ratio', 'EV To Sales', 'Enterprise Value Over EBITDA', 'EV To Operating Cash Flow', 'EV To Free Cash Flow', 'Earnings Yield', 'Free Cash Flow Yield', 'Debt To Equity', 'Debt To Assets', 'Net Debt To EBITDA', 'Current Ratio', 'Interest Coverage', 'Income Quality', 'Dividend Yield', 'Payout Ratio', 'Sales General And Administrative To Revenue', 'R&D To Revenue', 'Intangibles To Total Assets', 'Capex To Operating Cash Flow', 'Capex To Revenue', 'Capex To Depreciation', 'Stock Based Compensation To Revenue', 'Graham Number', 'ROIC', 'Return On Tangible Assets', 'GrahaM Net', 'Working Capital', 'Tangible Asset Value', 'Net Current Asset Value', 'Invested Capital', 'Average Receivables', 'Average Payables', 'Average Inventory', 'Days Sales Outstanding', 'Days Payables Outstanding', 'Days Of Inventory On Hand', 'Receivables Turnover', 'Payables Turnover', 'Inventory Turnover', 'ROE', 'Capex Per Share']
        df = pd.read_csv(self.quarterly_key_metrics.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def display_annual_key_metrics_statement(self):
        columns = ['Symbol', 'Date', 'Revenue Per Share', 'Net Income Per Share', 'Operating Cash Flow Per Share', 'Free Cash Flow Per Share', 'Cash Per Share', 'Book Value Per Share', 'Tangible Book Value Per Share', 'Shareholders Equity Per Share', 'Interest Debt Per Share', 'Market Cap', 'Enterprise Value', 'PE Ratio', 'Price To Sales Ratio', 'POCF Ratio', 'PFCF Ratio', 'PB Ratio', 'PTB Ratio', 'EV To Sales', 'Enterprise Value Over EBITDA', 'EV To Operating Cash Flow', 'EV To Free Cash Flow', 'Earnings Yield', 'Free Cash Flow Yield', 'Debt To Equity', 'Debt To Assets', 'Net Debt To EBITDA', 'Current Ratio', 'Interest Coverage', 'Income Quality', 'Dividend Yield', 'Payout Ratio', 'Sales General And Administrative To Revenue', 'R&D To Revenue', 'Intangibles To Total Assets', 'Capex To Operating Cash Flow', 'Capex To Revenue', 'Capex To Depreciation', 'Stock Based Compensation To Revenue', 'Graham Number', 'ROIC', 'Return On Tangible Assets', 'GrahaM Net', 'Working Capital', 'Tangible Asset Value', 'Net Current Asset Value', 'Invested Capital', 'Average Receivables', 'Average Payables', 'Average Inventory', 'Days Sales Outstanding', 'Days Payables Outstanding', 'Days Of Inventory On Hand', 'Receivables Turnover', 'Payables Turnover', 'Inventory Turnover', 'ROE', 'Capex Per Share']
        df = pd.read_csv(self.annual_key_metrics.path, names=columns)
        if len(df) == 0:
            return '<div class = "data-not-found"><i class="far fa-frown-open data-not-found-icon"></i><br>DATA NOT AVAILABLE</div>'
        else:
            df_hide_first_row = df.iloc[1:, 1:]
            data_table = df_hide_first_row.to_html(na_rep = '—', show_dimensions=True, border=0, index=True, index_names=False, header=True)
            return data_table

    def get_absolute_url(self):
        return reverse('stock-detail', kwargs={'slug': self.slug})

    def d_price(self):
        if len(self.price) < 1 or 'None' in self.price:
            return "—"
        else:
            return Decimal(self.price)

    def d_dayLow(self):
        if len(self.dayLow) < 1 or 'None' in self.dayLow:
            return "—"
        else:
            return Decimal(self.dayLow)

    def d_dayHigh(self):
        if len(self.dayHigh) < 1 or 'None' in self.dayHigh:
            return "—"
        else:
            return Decimal(self.dayHigh)

    def d_yearHigh(self):
        if len(self.yearHigh) < 1 or 'None' in self.yearHigh:
            return "—"
        else:
            return Decimal(self.yearHigh)

    def d_yearLow(self):
        if len(self.yearLow) < 1 or 'None' in self.yearLow:
            return "—"
        else:
            return Decimal(self.yearLow)

    def d_priceAvg50(self):
        if len(self.priceAvg50) < 1 or 'None' in self.priceAvg50:
            return "—"
        else:
            return Decimal(self.priceAvg50)

    def d_priceAvg200(self):
        if len(self.priceAvg200) < 1 or 'None' in self.priceAvg200:
            return "—"
        else:
            return Decimal(self.priceAvg200)

    def d_volume(self):
        if len(self.volume) < 1 or 'None' in self.volume:
            return "—"
        else:
            return int(self.volume)

    def d_avgVolume(self):
        if len(self.avgVolume) < 1 or 'None' in self.avgVolume:
            return "—"
        else:
            return int(self.avgVolume)

    def d_open(self):
        if len(self.openPrice) < 1 or 'None' in self.openPrice:
            return "—"
        else:
            return Decimal(self.openPrice)

    def d_previousClose(self):
        if len(self.previousClose) < 1 or 'None' in self.previousClose:
            return "—"
        else:
            return Decimal(self.previousClose)

    def d_eps(self):
        if len(self.eps) < 1 or 'None' in self.eps:
            return "—"
        else:
            return Decimal(self.eps)

    def d_sharesOutstanding(self):
        if len(self.sharesOutstanding) < 1 or 'None' in self.sharesOutstanding:
            return "—"
        else:
            return int(self.sharesOutstanding)

    def d_beta(self):
        if len(self.beta) < 1 or 'None' in self.beta:
            return "—"
        else:
            return Decimal(self.beta)

    def d_last_Div(self):
        if len(self.last_Div) < 1 or 'None' in self.last_Div:
            return "—"
        else:
            return Decimal(self.last_Div)

    def d_exchange(self):
        if len(self.exchange) <= 1 or 'None' in self.exchange:
            return "—"
        else:
            return self.exchange

    def d_exchangeShortName(self):
        if len(self.exchangeShortName) <= 1 or 'None' in self.exchangeShortName:
            return "—"
        else:
            return self.exchangeShortName

    def d_industry(self):
        if len(self.industry) <= 1 or 'None' in self.industry:
            return "—"
        else:
            return self.industry

    def d_website(self):
        if len(self.website) <= 1 or 'None' in self.website:
            return "—"
        else:
            return self.website

    def d_description(self):
        if len(self.description) <= 1 or 'None' in self.description:
            return "—"
        else:
            return self.description

    def d_ceo(self):
        if len(self.ceo) <= 1 or 'None' in self.ceo:
            return "—"
        else:
            return self.ceo

    def d_sector(self):
        if len(self.sector) <= 1 or 'None' in self.sector:
            return "—"
        else:
            return self.sector

    def d_country(self):
        if len(self.country) <= 1 or 'None' in self.country:
            return "—"
        else:
            return self.country

    def d_fullTimeEmployees(self):
        if len(self.fullTimeEmployees) <= 1 or 'None' in self.fullTimeEmployees:
            return "—"
        else:
            return int(self.fullTimeEmployees)

    def d_phone(self):
        if len(self.phone) <= 1 or 'None' in self.phone:
            return "—"
        else:
            return self.phone

    def d_city(self):
        if len(self.city) <= 1 or 'None' in self.city:
            return "—"
        else:
            return self.city

    def d_state(self):
        if len(self.state) <= 1 or 'None' in self.state:
            return "—"
        else:
            return self.state

    def d_zip(self):
        if len(self.zip) <= 1 or 'None' in self.zip:
            return "—"
        else:
            return self.zip

    def d_dcfDiff(self):
        if len(self.dcfDiff) < 1  or 'None' in self.dcfDiff:
            return "—"
        else:
            return Decimal(self.dcfDiff)

    def d_dcf(self):
        if len(self.dcf) < 1 or 'None' in self.dcf:
            return "—"
        else:
            return Decimal(self.dcf)

    def d_pe(self):
        if 'None' in self.eps:
            return "—"
        else:
            return self.d_price() / self.d_eps()

    def d_change(self):
        return (self.d_price() - self.d_previousClose())

    def d_change_percentage(self):
        return ((self.d_price() - self.d_previousClose()) / self.d_previousClose()) * 100

    def d_market_cap(self):
        return self.d_price() * self.d_sharesOutstanding()

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.symbol)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug = slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug, randstr = random_string_generator(size = 4))

        return unique_slug_generator(instance, new_slug = new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender = Stock)
