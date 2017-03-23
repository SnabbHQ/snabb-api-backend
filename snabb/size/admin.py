# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Size, MinimumPrice


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'size_city', 'size_price', 'active']
    list_filter = ['size_city', 'active']


class MinimumPriceAdmin(admin.ModelAdmin):
    list_display = ['size', 'price_city', 'price_value', 'price_meters', 'active']
    list_filter = ['price_city', 'active']

admin.site.register(Size, SizeAdmin)
admin.site.register(MinimumPrice, MinimumPriceAdmin)
