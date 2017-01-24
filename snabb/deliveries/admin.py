# encoding:utf-8

from django.contrib import admin
from .models import Delivery, Quote, Location

admin.site.register(Delivery)
admin.site.register(Quote)
admin.site.register(Location)
