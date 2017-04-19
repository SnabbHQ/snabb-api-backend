import json
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.users.models import Profile
from snabb.billing.views import ReceiptUserViewSet, ReceiptCourierViewSet
from snabb.utils.setup_tests import create_profile


class ReceiptsUserTests(APITestCase):

    def test_get_receipts(self):
        """ Test get receipts from a user """
        user = create_profile()

        factory = APIRequestFactory()
        request = factory.get('/api/v1/billing/receiptsUser/')
        view = ReceiptUserViewSet.as_view({'get': 'list'})

        '''
        # Without Auth -- User
        response = view(request)
        self.assertEqual(response.status_code, 401)
        '''

        # With Auth -- User
        force_authenticate(request, user=user.profile_apiuser)
        response = view(request)
        self.assertEqual(response.status_code, 200)


class ReceiptsCourierTests(APITestCase):

    def test_get_receipts(self):
        """ Test get receipts from a user """
        user = create_profile()

        factory = APIRequestFactory()
        request = factory.get('/api/v1/billing/receiptsCourier/')
        view = ReceiptCourierViewSet.as_view({'get': 'list'})

        '''
        # Without Auth -- Courier
        response = view(request)
        self.assertEqual(response.status_code, 401)

        # With Auth -- Courier
        force_authenticate(request, user=user.profile_apiuser)
        view = ReceiptCourierViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 401)
        '''

        # Check if user is admin
        user.is_staff = True
        user.is_admin = True
        user.save()
        force_authenticate(request, user=user.profile_apiuser)
        view = ReceiptCourierViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
