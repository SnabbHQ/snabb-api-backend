from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from snabb.location.models import Zipcode, City
from django.conf import settings


class ProfileTests(APITestCase):
    def create_zipcode(self, code, city, active):
        zipcode = Zipcode.objects.get_or_create(
            code=code, zipcode_city=city, active=active
        )
        return zipcode[0]

    def create_city(self, name, active):
        city = City.objects.get_or_create(
            name=name, active=active
        )
        return city[0]

    def test_verify_address(self):
        """ Ensure we can verify an address by zipcode. """
        return 0
        url = reverse('validateAddress')

        city = self.create_city('Valencia', True)
        zipcode = self.create_zipcode(46800, city, True)
        zipcode = self.create_zipcode(46801, city, False)

        city = self.create_city('Alicante', False)
        zipcode = self.create_zipcode(46700, city, True)
        zipcode = self.create_zipcode(46701, city, False)

        data = {'zipcode': 46800, 'city': 'Valencia'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 200204)
        self.assertEqual(response.data['data']['key'], 'ADDRESS_OK')

        data = {'zipcode': 46801, 'city': 'Valencia'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400208)
        self.assertEqual(response.data['data']['key'], 'INACTIVE_ZIPCODE')

        data = {'zipcode': 999, 'city': 'Albaida'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400207)
        self.assertEqual(response.data['data']['key'], 'INVALID_ADDRESS')

        data = {'zipcode': 46700, 'city': 'Muro'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400207)
        self.assertEqual(response.data['data']['key'], 'INVALID_ADDRESS')

        data = {'zipcode': 46700, 'city': 'Alicante'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400209)
        self.assertEqual(response.data['data']['key'], 'INACTIVE_CITY')

        data = {'zipcode': 46701, 'city': 'Alicante'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400208)
        self.assertEqual(response.data['data']['key'], 'INACTIVE_ZIPCODE')

        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400205)
        self.assertEqual(response.data['data']['key'], 'KEY_ZIPCODE_REQUIRED')

        data = {'zipcode': 123}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400206)
        self.assertEqual(response.data['data']['key'], 'KEY_CITY_REQUIRED')
