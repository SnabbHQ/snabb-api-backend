# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Zipcode, City, Region, Country
from snabb.size.models import Size


class SizeInline(admin.TabularInline):
    model = Size
    extra = 0


class ZipcodeInline(admin.TabularInline):
    model = Zipcode
    extra = 0


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_filter = ['active']
    inlines = [SizeInline, ZipcodeInline]


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'country_currency', 'active']
    list_filter = ['active', ]


class ZipcodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'zipcode_city', 'active']
    list_filter = ['active', ]


admin.site.register(Zipcode, ZipcodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Region)
admin.site.register(Country, CountryAdmin)
