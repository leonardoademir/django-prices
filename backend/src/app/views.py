from django.shortcuts import render
import requests
from pandas.tseries.offsets import BDay
from datetime import date
from django.http import JsonResponse
from django.views import View

class PriceController(View):
    def get(self, request, *args, **kwargs):
        today = date.today()
        data = []

        for i in range(5):
            params = {'date': today.strftime('%Y-%m-%d') if i == 0 else (today - BDay(i)).strftime('%Y-%m-%d'),
                      'symbols': 'EUR,BRL,JPY',
                      'base': 'USD'
                      }
            response = requests.get('https://api.vatcomply.com/rates?', params)
            data.append(response.json())

        return JsonResponse(data, safe=False)