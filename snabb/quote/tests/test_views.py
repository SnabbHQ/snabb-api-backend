import json
from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    force_authenticate
)

from snabb.quote.views import QuoteViewSet
from snabb.quote.tests.json import test1, test2, test3, test4
from snabb.utils.setup_tests import (
    create_profile,
    init_data_geo,
    post_api
)


class QuoteTests(APITestCase):

    def test_create_quote(self):
        """ Test create a quote """
        # Init Data
        init_data_geo()
        user = create_profile()

        # Test Cases
        response = post_api(
            user, test1.data, '/api/v1/deliveries/quote', QuoteViewSet)
        self.assertEqual(response.status_code, 200)

        response = post_api(user, {}, '/api/v1/deliveries/quote', QuoteViewSet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400300)

        response = post_api(
            user, test2.data, '/api/v1/deliveries/quote', QuoteViewSet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400305)

        response = post_api(
            user, test3.data, '/api/v1/deliveries/quote', QuoteViewSet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400407)

        response = post_api(
            user, test4.data, '/api/v1/deliveries/quote', QuoteViewSet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400311)
