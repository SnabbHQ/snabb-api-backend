# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
from django.db import models


def _create_hash():
    """This function generate 10 character long hash"""
    hash_value = hashlib.sha1()
    hash_value.update(str(time.time()).encode('utf8'))
    return hash_value.hexdigest()[:-20]
