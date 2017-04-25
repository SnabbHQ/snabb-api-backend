import json
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from snabb.users.models import Profile
from snabb.utils.setup_tests import (
    create_profile, create_token_card, post_api, patch_api
)
from snabb.payment.views import CardViewSet
from snabb.payment.models import Card
import stripe


class CardsTests(APITestCase):

    def test_create_card(self):

        """ Test get receipts from a user """
        user = create_profile()

        # Create a card
        data_card_1 = {
            "number": '4242424242424242',
            "exp_month": 12, "exp_year": 2017, "cvc": '123'
        }
        data_card_2 = {
            "number": '5555555555554444',
            "exp_month": 12, "exp_year": 2017, "cvc": '123'
        }
        data_card_3 = {
            "number": '378282246310005',
            "exp_month": 12, "exp_year": 2017, "cvc": '123'
        }

        # Test Cases

        # Without token
        response = post_api(user, {}, '/api/v1/cards', CardViewSet)
        self.assertEqual(response.data['code'], 400600)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # With invalid token
        data = { 'token': '123456789' }
        response = post_api(user, data, '/api/v1/cards', CardViewSet)
        self.assertEqual(response.data['code'], 400604)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # With valid token
        token = create_token_card(data_card_1)
        data = { 'token': token }
        response = post_api(user, data, '/api/v1/cards', CardViewSet)
        self.assertEqual(response.data['code'], 200208)
        self.assertEqual(response.status_code, 200)

        token = create_token_card(data_card_2)
        data = { 'token': token }
        response = post_api(user, data, '/api/v1/cards', CardViewSet)
        self.assertEqual(response.data['code'], 200208)
        self.assertEqual(response.status_code, 200)

        token = create_token_card(data_card_3)
        data = { 'token': token }
        response = post_api(user, data, '/api/v1/cards', CardViewSet)
        self.assertEqual(response.data['code'], 200208)
        self.assertEqual(response.status_code, 200)

        '''
        # Change default card
        card_id = str(Card.objects.all()[1].card_id)
        data = { 'card_id':card_id, 'default_card': False }
        response = patch_api(user, data, '/api/v1/cards/'+card_id+'/', CardViewSet)
        self.assertEqual(response.data['code'], 200208)
        data = { 'card_id':card_id, 'default_card': True }
        response = patch_api(user, data, '/api/v1/cards/'+card_id+'/', CardViewSet)
        self.assertEqual(response.status_code, 200)
        '''
