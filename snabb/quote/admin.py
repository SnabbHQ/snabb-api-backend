# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Quote, Task, Place


class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ['quote_id', 'quote_user', 'active']
    list_filter = ['active']
    readonly_fields = ['prices']


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['task_id', 'task_type', 'active']
    list_filter = ['active']
    readonly_fields = ['task_detail']


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ['place_id', 'place_address',
                    'description', 'active']
    list_filter = ['active']


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Place, PlaceAdmin)
