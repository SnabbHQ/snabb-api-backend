from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from snabb.location.models import Zipcode
from django.conf import settings


class ProfileTests(APITestCase):
    def create_zipcode(self):
        zipcode = Zipcode.objects.get_or_create(code=46860)
        return zipcode[0]

    def test_verify_address(self):
        """ Ensure we can verify an address by zipcode. """

        url = reverse('validateAddress')
        zipcode = self.create_zipcode()

        data = {'zipcode': 46860}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 200204)
        self.assertEqual(response.data['data']['key'], 'ADDRESS_OK')

        data = {'zipcode': 999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400204)
        self.assertEqual(response.data['data']['key'], 'ADDRESS_NOT_VALID')

        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400205)
        self.assertEqual(response.data['data']['key'], 'KEY_ZIPCODE_REQUIRED')
