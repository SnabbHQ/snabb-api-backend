from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.location.models import Zipcode, City, Country, Region
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from snabb.users.models import Profile
from rest_framework.authtoken.models import Token
from snabb.quote.views import QuoteViewSet
import json



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

    def test_create_quote(self):
        """ Test create a quote """

        # Init Data
        country_es = self.create_country('Spain', 'ES', True)
        region_valencia = self.create_region(
            'Valencia', 'Comunidad Valenciana', country_es, True
        )
        city = self.create_city(
             'Albaida', 'Albaida', region_valencia, True
        )
        zipcode = self.create_zipcode(46860, city, True)

        user = self.create_profile()




        #request = APIRequestFactory().post("")
        #view = QuoteViewSet.as_view({'post': 'create'})

        #print (user)
        #print (user.profile_apiuser)


        data = {
            "tasks" : [
            {
              "type": "pickup",
              "comments": "hay que enviarse urgentemente",
              "place":{
                "description" : "esto es un paquete super grande.",
                "address": "Santa Ana 22, Albaida, 46860, Spain"
              },
              "contact":{
                "first_name": "Jose Luís",
                "last_name": "Camacho",
                "company_name": "navilo",
                "phone": 555555,
                "email": "test@test.com"
              }
            },
            {
              "type": "dropoff",
              "comments": "esto es un comentario de prueba",
              "place":{
                "description" : "esperando que llegue",
                "address": "Santa Ana 22, Albaida, 46860, Spain"
              },
              "contact":{
                "first_name": "Mariano",
                "last_name": "Rajoy",
                "company_name": "pp",
                "phone": 666,
                "email": "pp@pp.ppp"
              }
            }
          ]
        }


        factory = RequestFactory()
        request = factory.post(
            '/api/v1/deliveries/quote',
            json.dumps(data),
            content_type='application/json'
        )

        force_authenticate(request, user=user.profile_apiuser)
        view = QuoteViewSet.as_view({'post': 'create'})
        response = view(request)

        print (response)
        print('-------------------------')
        print(response.data)
        #print(response.data['code'])
        #print('-------------------------')


        #self.assertEqual(response.data['code'], 400300)




        self.assertEqual(response.status_code, 200)
