from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.location.models import Zipcode, City
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from snabb.users.models import Profile
from rest_framework.authtoken.models import Token


class QuoteTests(APITestCase):
    '''
    def create_profile(self):
        profile = Profile.objects.get_or_create(company_name='My Company S.L.',
                                                email='email@example.com',
                                                password='123456',
                                                phone='+34123456789',
                                                user_lang='es'
                                                )
        return profile[0]

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

    def test_create_quote(self):
        """ Test create a quote """

        url = reverse('validateAddress')
        print('\n ********* \n')
        print(url)
        print('\n ********* \n')

        city = self.create_city('Valencia', True)
        zipcode = self.create_zipcode(46800, city, True)
        zipcode = self.create_zipcode(46801, city, False)

        city = self.create_city('Alicante', False)
        zipcode = self.create_zipcode(46700, city, True)
        zipcode = self.create_zipcode(46701, city, False)

        data = {'zipcode': 46800, 'city': 'Valencia'}
        header = {}
        response = self.client.post(url, data, format='json')

        user = self.create_profile()

        new_token = Token.objects.create(user=user.profile_apiuser)


        # Include an appropriate `Authorization:` header on all requests.

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


        self.assertEqual(response.data['data']['code'], 200204)
        self.assertEqual(response.data['data']['key'], 'ADDRESS_OK')

        url = '/api/quote'
        #profile = self.create_profile()
        data = {}

        response = self.client.post(url, data, format='json')
        print('\n ********* \n')
        print(response)
        print('\n ********* \n')
        # self.assertEqual(response.data, 400301)
    '''
