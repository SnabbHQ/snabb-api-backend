# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Size


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'size_city', 'size_price', 'active']
    list_filter = ['size_city', 'active']

admin.site.register(Size, SizeAdmin)
