from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from snabb.location.models import Zipcode, City, Region, Country


class ProfileTests(APITestCase):
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

    def create_region(self, name, google_short_name, region_country, active):
        region = Region.objects.get_or_create(
            name=name, active=active,
            google_short_name=google_short_name
        )
        return region[0]

    def create_country(self, name, iso_code, active):
        country = Country.objects.get_or_create(
            name=name, iso_code=iso_code, active=active
        )
        return country[0]

    def test_verify_address(self):
        """ Ensure we can verify an address by an address in Google. """

        url = reverse('validateAddress')

        # Create Country
        country_es = self.create_country('Spain', 'ES', True)
        country_ita = self.create_country('Italia', 'ITA', False)
        country_pa = self.create_country('Panama', 'PA', True)

        # Create Region
        region_valencia = self.create_region(
            'Valencia', 'Comunidad Valenciana', country_es, True
        )
        region_castilla_mancha = self.create_region(
            'Castilla la Mancha', 'CM', country_es, False
        )
        region_panama = self.create_region(
            'Panamá', 'Panamá', country_pa, True
        )
        region_provincia_chiriqui = self.create_region(
            'Provincia de Chiriquí', 'Provincia de Chiriquí', country_pa, True
        )

        # Create City
        city_albaida = self.create_city(
            'Albaida', 'Albaida', region_valencia, True
        )
        city_ontinyent = self.create_city(
            'Ontinyent', 'Ontinyent', region_valencia, True
        )
        city_panama = self.create_city(
            'Panamá', 'Panamá', region_valencia, True
        )

        # Create Zipcode
        zipcode_albaida = self.create_zipcode(46860, city_albaida, True)
        zipcode_ontinyent = self.create_zipcode(46870, city_ontinyent, False)

        # Test cases
        data = {'address': 'Santa Ana 22, Albaida, 46860, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 200206)

        data = {'address': 'Calle 66 Este, Panama, Panama'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 200206)

        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400401)

        data = {'address': 'Calle Washington 99, Albaida, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400407)

        data = {'address': 'Albaida, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400402)

        data = {'address': 'Via Schubert, Roma, Italy'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400403)

        data = {'address': 'Avenida Albaida, Ontinyent, 46870, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400405)

        data = {'address': 'Calle los abanicos, David, Panama'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['data']['code'], 400406)
