from django.shortcuts import render
import requests
from pandas.tseries.offsets import BDay
from datetime import date
from django.http import JsonResponse
from django.views import View
from app.models import PriceModel

class PriceController(View):
    def get(self, request, *args, **kwargs):
        today = date.today()
        data = []


        for i in range(5):
            #Preparando parametros (data atual, apenas dias úteis, símbolos e base)
            params = {'date': today.strftime('%Y-%m-%d') if i == 0 else (today - BDay(i)).strftime('%Y-%m-%d'),
                      'symbols': 'EUR,BRL,JPY',
                      'base': 'USD'
                      }
            response = requests.get('https://api.vatcomply.com/rates?', params)

            #Gravar dados no banco
            for rate in response.json()['rates'].items():
                try:
                    price_exists = PriceModel.objects.filter(date=response.json()['date'], currency=rate[0])
                    if len(price_exists) == 0:
                        price = PriceModel.objects.create(currency=rate[0], date=response.json()['date'],value=float(rate[1]))
                except Exception as e:
                    print(str(e))

            data.append(response.json())

        return JsonResponse(data, safe=False)