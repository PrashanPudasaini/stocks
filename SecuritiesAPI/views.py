from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StockSerializer
from Securities.models import Stock

@api_view(['GET'])
def apiOverview(request):
    securities_api_urls = {
        'List': '/stock-list/',
        'Detail': '/symbol/<slug:slug>/',
        'Create': '/stock-create/',
    }
    return Response(securities_api_urls)

# Query the database, serialize the present objects and data, and then return it in our api response
@api_view(['GET'])
def stockList(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def stockCreate(request):
    serializer = StockSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def stockDetail(request, slug):
    stocks = Stock.objects.get(slug=slug)
    serializer = StockSerializer(stocks, many = False)

    return Response(serializer.data)
