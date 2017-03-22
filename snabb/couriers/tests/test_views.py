from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from snabb.users.models import Profile
from django.conf import settings
