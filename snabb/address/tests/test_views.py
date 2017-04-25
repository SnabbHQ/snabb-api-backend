from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from snabb.utils.setup_tests import (
    create_country,
    create_region,
    create_city,
    create_zipcode,
    create_currency
)


class ProfileTests(APITestCase):

    def test_verify_address(self):
        """ Ensure we can verify an address by an address in Google. """

        url = reverse('validateAddress')

        # Create Country
        currency = create_currency('Euro', '€', 'EUR', True)
        country_es = create_country('Spain', 'ES', True, currency)
        country_ita = create_country('Italia', 'ITA', False, currency)
        country_pa = create_country('Panama', 'PA', True, currency)

        # Create Region
        region_valencia = create_region(
            'Valencia', 'Comunidad Valenciana', country_es, True
        )
        region_castilla_mancha = create_region(
            'Castilla la Mancha', 'CM', country_es, False
        )
        region_panama = create_region(
            'Panamá', 'Panamá', country_pa, True
        )
        region_provincia_chiriqui = create_region(
            'Provincia de Chiriquí', 'Provincia de Chiriquí', country_pa, True
        )

        # Create City
        city_albaida = create_city(
            'Albaida', 'Albaida', region_valencia, True
        )
        city_ontinyent = create_city(
            'Ontinyent', 'Ontinyent', region_valencia, True
        )
        city_panama = create_city(
            'Panamá', 'Panamá', region_valencia, True
        )

        # Create Zipcode
        zipcode_albaida = create_zipcode(46860, city_albaida, True)
        zipcode_ontinyent = create_zipcode(46870, city_ontinyent, False)

        # Test cases
        data = {'address': 'Santa Ana 22, Albaida, 46860, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200206)

        data = {'address': 'Calle 66 Este, Panama, Panama'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200206)

        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400401)

        data = {'address': 'Calle Washington 99, Albaida, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400407)

        data = {'address': 'Albaida, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400402)

        data = {'address': 'Via Schubert, Roma, Italy'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400403)

        data = {'address': 'Avenida Albaida, Ontinyent, 46870, Spain'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400405)

        data = {'address': 'Calle los abanicos, David, Panama'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400406)
