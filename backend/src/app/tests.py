# test_models.py
from app.models import PriceModel
from django.test import TestCase
import requests

class PriceModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        PriceModel.objects.create(currency="BRL", date="2022-03-05", value=4.54545)

    def test_price_values(self):
        price = PriceModel.objects.get(date="2022-03-05")
        
        self.assertEqual(price.value, 4.54545, "Not Equal")

    def test_creation_validation(self):
        with self.assertRaises(Exception):
            price_test = PriceModel.objects.create(currency="BRL", date="2022-03-05", value='teste')

class UrlTestCase(TestCase):
    def test_url_ok(self):
        response = requests.get('https://api.vatcomply.com/rates?')
        self.assertEqual(response.status_code, 200)
    
    def test_url_wrong_params(self):
        params = {'symbols': 'ZZZ',
                      'base': 'USD'
                      }
        response = requests.get('https://api.vatcomply.com/rates?', params)
        self.assertEqual(response.status_code, 400)