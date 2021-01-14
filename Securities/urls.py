from django.urls import path
from .views import HomePageView, StockCreateView, StockListView, StockDetailView, MarketsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('stocks/markets/', MarketsView.as_view(), name='markets'),
    path('stocks/search/', StockCreateView.as_view(), name='stock-search'),
    path('stocks/most-popular-stocks', StockListView.as_view(), name='stock-most-popular'),
    path('stocks/<slug:slug>/', StockDetailView.as_view(), name='stock-detail'),
]
