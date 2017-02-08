# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Quote, DropOff, Pickup


class DropOffInline(admin.TabularInline):
    model = DropOff
    extra = 0


class PickupInline(admin.TabularInline):
    model = Pickup
    extra = 0


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_id', 'active', 'prices']
    list_filter = ['active']
    inlines = [DropOffInline, PickupInline]


admin.site.register(Quote, QuoteAdmin)
admin.site.register(DropOff)
admin.site.register(Pickup)
