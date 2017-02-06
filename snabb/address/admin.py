# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Address, AddressBook

admin.site.register(Address)
admin.site.register(AddressBook)
