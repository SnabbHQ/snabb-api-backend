import json
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.location.models import Zipcode, City, Country, Region
from snabb.users.models import Profile
from snabb.quote.views import QuoteViewSet
from snabb.quote.tests.json import test1, test2, test3, test4


class QuoteTests(APITestCase):

    def create_profile(self):
        profile = Profile.objects.get_or_create(company_name='My Company S.L.',
                                                email='email@example.com',
                                                password='123456',
                                                phone='+34123456789',
                                                user_lang='es'
                                                )
        return profile[0]

    def create_country(self, name, iso_code, active):
        country = Country.objects.get_or_create(
            name=name, iso_code=iso_code, active=active
        )
        return country[0]

    def create_region(self, name, google_short_name, region_country, active):
        region = Region.objects.get_or_create(
            name=name, active=active,
            google_short_name=google_short_name
        )
        return region[0]

    def create_zipcode(self, code, city, active):
        zipcode = Zipcode.objects.get_or_create(
            code=code, zipcode_city=city, active=active
        )
        return zipcode[0]

    def create_city(self, name, google_short_name, region, active):
        city = City.objects.get_or_create(
            name=name, active=active,
            google_short_name=google_short_name,
        )
        return city[0]

    def init_data_geo(self):
        country = self.create_country('Spain', 'ES', True)
        region_valencia = self.create_region(
            'Valencia', 'Comunidad Valenciana', country, True)
        city = self.create_city(
             'Albaida', 'Albaida', region_valencia, True)
        zipcode = self.create_zipcode(46860, city, True)

    def post_api(self, user, data):
        factory = APIRequestFactory()
        request = factory.post(
            '/api/v1/deliveries/quote',
            json.dumps(data), content_type='application/json'
        )
        force_authenticate(request, user=user.profile_apiuser)
        view = QuoteViewSet.as_view({'post': 'create'})
        response = view(request)
        return response


    def test_create_quote(self):
        """ Test create a quote """
        # Init Data
        self.init_data_geo()
        user = self.create_profile()

        # Test Cases
        response = self.post_api(user, test1.data)
        self.assertEqual(response.status_code, 200)

        response = self.post_api(user, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400300)

        response = self.post_api(user, test2.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400305)

        response = self.post_api(user, test3.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400407)

        response = self.post_api(user, test4.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400311)
