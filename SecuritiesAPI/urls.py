from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name = "api-overview"),
    path('stock-list/', views.stockList, name = "stock-list"),
    path('stock-create/', views.stockCreate, name = "stock-create"),
    path('symbol/<slug:slug>/', views.stockDetail, name = "symbol"),
]
