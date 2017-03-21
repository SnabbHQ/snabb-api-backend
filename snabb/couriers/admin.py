# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Team, Courier


class TeamAdmin(admin.ModelAdmin):

    model = Team
    list_display = ['name']
    readonly_fields = ('team_onfleet_id',)


class CourierAdmin(admin.ModelAdmin):

    model = Team
    list_display = ['name']
    readonly_fields = ('courier_onfleet_id', 'courier_details')

admin.site.register(Team, TeamAdmin)
admin.site.register(Courier, CourierAdmin)
