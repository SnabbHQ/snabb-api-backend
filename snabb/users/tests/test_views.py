from django.test import RequestFactory
from test_plus.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from snabb.users.models import Profile
from django.conf import settings
from snabb.utils.setup_tests import create_profile


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class ProfileTests(APITestCase):

    def test_create_profile(self):
        """
        Ensure we can register a new user.
        """
        # Set to test sending email.
        url = reverse('register_user')

        # User without all fields.
        data = {'company_name': 'My Company S.L.', 'email': 'email2@example.com',
                'phone': '+34666555777', 'user_lang': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_AND_PASSWORD_REQUIRED')

        # User with invalid password.
        data = {'company_name': 'My Company S.L.', 'email': 'email2@example.com',
                'password': '12345', 'phone': '+34666555777', 'user_lang': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'PASSWORD_WRONG')

        # User with invalid email.
        data = {'company_name': 'My Company S.L.', 'email': 'email2@example',
                'password': '123456', 'phone': '+34666555777', 'user_lang': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_WRONG')

        # Right User
        data = {'company_name': 'My Company S.L.', 'email': 'email@example.com',
                'password': 'p4ssword', 'phone': '+34666555777', 'user_lang': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().email, 'email@example.com')

        # Same user as first.
        data = {'company_name': 'My Company S.L.', 'email': 'email@example.com',
                'password': 'p4ssword', 'phone': '+34666555777', 'user_lang': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_ALREADY_EXISTS')

    def test_verify_account(self):
        """
        Ensure we can verify user account.
        """
        url = reverse('verify_user')

        profile = create_profile()

        # Without hash
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'HASH_REQUIRED')

        # With non-existent hash
        data = {'hash': 'fdsdfserwasdasd'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'HASH_NOT_EXISTS')

        # With right hash
        data = {'hash': profile.profile_activation_key}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], 'VERIFY_OK')

        # Retry to verify same user
        data = {'hash': profile.profile_activation_key}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'ALREADY_VERIFIED')

    def test_send_verify_email(self):
        """
        Ensure we can send email to user with a verify_user hash.
        """
        url = reverse('send_verify_email')
        url_verify = reverse('verify_user')

        profile = create_profile()

        # Without email
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_REQUIRED')

        # With non-existent email
        data = {'email': 'my-example@my-domain.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_NOT_EXISTS')

        # With right email
        data = {'email': profile.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], 'SEND_EMAIL_OK')

        # Verify user for next test.
        data = {'hash': profile.profile_activation_key}
        response = self.client.post(url_verify, data, format='json')

        # Retry to already verified user
        data = {'email': profile.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'ALREADY_VERIFIED')

    def test_forgot_password(self):
        """
        Ensure we can send email to user with a reset_password hash.
        """
        url = reverse('forgot_password')
        profile = create_profile()

        # Without email
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_REQUIRED')

        # With non-existent email
        data = {'email': 'my-example@my-domain.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'EMAIL_NOT_EXISTS')

        # With right email
        data = {'email': profile.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], 'SEND_EMAIL_OK')

    def test_reset_password(self):
        """
        Ensure we can reset user password.
        """
        url = reverse('reset_password')

        profile = create_profile()

        # Without hash
        data = {"password": "p4ssw0rd"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'HASH_PASSWORD_REQUIRED')

        # Without password
        data = {"hash": "sfsdf9s6df9s6df"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'HASH_PASSWORD_REQUIRED')

        # With non-existent hash
        data = {'hash': 'fdsdfserwasdasd', "password": "p4ssw0rd"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['key'], 'HASH_NOT_EXISTS')

        # With right hash and password
        data = {'hash': profile.reset_password_key, "password": "p4ssw0rd"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], 'RESET_OK')
