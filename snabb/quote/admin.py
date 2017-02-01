# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Quote, QuotePrice


admin.site.register(Quote)
admin.site.register(QuotePrice)
