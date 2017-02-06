# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Quote, DropOff, Pickup

admin.site.register(Quote)
admin.site.register(DropOff)
admin.site.register(Pickup)
