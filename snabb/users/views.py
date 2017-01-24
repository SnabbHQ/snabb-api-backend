# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
import uuid
import re


def _check_email(email):
    """This function parse if email is valid."""
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return EMAIL_REGEX.match(email)


def _check_password(password):
    """This function parse if password is valid. At least 6 characters long ."""
    # We add this inside a function, because we
    # can add more checks for this field in the future.
    if len(password) >= 6:
        return True
    else:
        return False


class RegisterUser(APIView):

    """
    API endpoint that allows to register new user.
    """
    # permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    permission_classes = (AllowAny,)

    def get_object(self, email):
        try:
            return Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            return False

    def post(self, request, format=None):

        received = request.data

        if ('email' in received.keys() and
                'password' in received.keys() and
                'company_name' and 'phone' in received.keys()):

            current_user = self.get_object(
                received['email'].lower()
            )

            if not _check_email(received['email'].lower()):
                return Response(
                    data={
                        'code': 400101,
                        'message': 'Invalid email.',
                        'key': 'EMAIL_WRONG'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not _check_password(received['password']):
                return Response(
                    data={
                        'code': 400102,
                        'message': 'Password must be at least 6 chars long.',
                        'key': 'PASSWROD_WRONG'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if current_user is False:
                user = Profile()
                user.email = received['email'].lower().replace(" ", "")
                user.password = received['password']
                user.phone = received['phone']
                user.company_name = received['company_name']

                if 'user_lang' in received.keys():
                    user.user_lang = received['user_lang']

                # Generate Hash for activation
                user.profile_activation_key = "%s" % (uuid.uuid4(),)
                user.save()

                # Generate activation link
                # Pending to define frontend url to redirect form email.
                url_validate = 'activate/' + user.profile_activation_key

                # Send email activacion
                '''
                email_instance = Email()
                email_instance.sendemail_activate_account(
                    user.email, url_validate
                )
                '''
                serializer = ProfileSerializer(
                    user, context={'request': request}, partial=True)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(
                    data={
                        'code': 400103,
                        'message': 'Email already exists',
                        'key': 'EMAIL_ALREADY_EXISTS'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data={
                    'code': 400104,
                    'message': 'Company Name, Email, phone and password required',
                    'key': 'EMAIL_AND_PASSWORD_REQUIRED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyUser(APIView):

    """
    API endpoint that allows to verify user email.
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data

        if ('hash' in received.keys()):
            key = received['hash']
        else:
            return Response(
                data={
                    'code': 400105,
                    'message': 'User hash required',
                    'key': 'HASH_REQUIRED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Profile.objects.get(profile_activation_key=key)
        except Profile.DoesNotExist:
            return Response(
                data={
                    'code': 400106,
                    'message': 'Hash not exists',
                    'key': 'HASH_NOT_EXISTS'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.verified:
            return Response(
                data={
                    'code': 400107,
                    'message': 'This user is already verified',
                    'key': 'ALREADY_VERIFIED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.profile_activation_key == key and user.verified is False:
            user.verified = True
            user.save()
            return Response(
                data={
                    'code': 200101,
                    'message': 'Email verified',
                    'key': 'VERIFY_OK'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'code': 400108,
                    'message': 'An error has occurred',
                    'key': 'VERIFY_ERROR'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Profile to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request):
        try:
            profile = Profile.objects.get(profile_apiuser=self.request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.none()

        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def get_object(self):
        try:
            profile = Profile.objects.get(profile_apiuser=self.request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.none()
        return profile

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(profile_apiuser=self.request.user)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
