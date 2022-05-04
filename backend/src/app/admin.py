from django.contrib import admin
from app.models import PriceModel


class PriceAdmin(admin.ModelAdmin):
    list_display= ('currency', 'date', 'value')
    
  
admin.site.register(PriceModel, PriceAdmin)
