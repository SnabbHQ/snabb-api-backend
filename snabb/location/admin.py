# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Zipcode, City, Region, Country, Address

admin.site.register(Zipcode)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Address)
