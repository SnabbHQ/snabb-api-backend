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
    init_data_geo
)


class QuoteTests(APITestCase):

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
        init_data_geo()
        user = create_profile()

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
