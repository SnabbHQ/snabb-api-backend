# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Quote, Task, Place


class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ['quote_id', 'active']
    list_filter = ['active']
    readonly_fields = ['prices']


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['task_id', 'active']
    list_filter = ['active']


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Place)
