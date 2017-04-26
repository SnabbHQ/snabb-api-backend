import json
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.users.models import Profile
from snabb.deliveries.views import DeliveryViewSet
from snabb.utils.setup_tests import create_profile, create_quote, post_api, init_data_geo
from snabb.deliveries.models import Delivery


class DeliveryTests(APITestCase):

    def create_delivery(self, user, quote):
        factory = APIRequestFactory()
        data = {'quote_id': quote.data['quote_id'],
                'selected_package_size': 'small'}
        response = post_api(
            user, data, '/api/v1/deliveries/delivery', DeliveryViewSet)
        return response

    def test_create_delivery(self):
        user = create_profile()
        new_quote = create_quote(user)
        # Test new delivery
        delivery = self.create_delivery(user, new_quote)
        self.assertEqual(delivery.status_code, 200)

        # Delivery with same quote
        delivery = self.create_delivery(user, new_quote)
        self.assertEqual(delivery.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_delivery(self):
        user = create_profile()
        new_quote = create_quote(user)
        delivery_1 = self.create_delivery(user, new_quote)
        new_quote = create_quote(user)
        delivery_2 = self.create_delivery(user, new_quote)

        # Test list
        factory = APIRequestFactory()
        request = factory.get(
            '/api/v1/deliveries/delivery'
        )
        force_authenticate(request, user=user.profile_apiuser)
        view = DeliveryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, 200)

        # Test filters by status
        current_delivery = Delivery.objects.get(
            delivery_id=delivery_2.data['delivery_id'])
        current_delivery.status = 'assigned'
        current_delivery.save()
        request = factory.get(
            '/api/v1/deliveries/delivery?status=assigned'
        )
        force_authenticate(request, user=user.profile_apiuser)
        view = DeliveryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, 200)
