# -*- coding: utf-8 -*-
"""
Development Configurations

"""

from .production import *  # noqa

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# To allow using http as well. (At least for now).
SESSION_COOKIE_SECURE = False

# APP SETTINGS
# ------------------------------------------------------------------------------
# In develop environment, lets enable DEBUG in order to get better stack traces of errors.
ALLOWED_HOSTS = ['*']
DEBUG = env.bool('DJANGO_DEBUG', default=True)
