# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
# Imports for welcome email.
from snabb.email_utils.views import send_mail_template


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
                        'key': 'PASSWORD_WRONG'
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

                user.save()

                # Substitutions for Sendgrid mail
                substitutions = {}
                substitutions['%user_link%'] = 'activate/' + user.profile_activation_key
                substitutions['%name%'] = user.company_name
                template = '55345630-06db-4987-863d-9189b0e97b57'

                # Send email welcome with activation link
                send_mail_template(user, template, substitutions)

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


class SendVerifyEmail(APIView):

    """
    API endpoint that allows to resend verify user email.
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data

        if ('email' in received.keys()):
            email = received['email']
        else:
            return Response(
                data={
                    'code': 400109,
                    'message': 'Email required',
                    'key': 'EMAIL_REQUIRED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            return Response(
                data={
                    'code': 400110,
                    'message': 'Email not exists',
                    'key': 'EMAIL_NOT_EXISTS'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.verified:
            return Response(
                data={
                    'code': 400111,
                    'message': 'This user is already verified',
                    'key': 'ALREADY_VERIFIED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            substitutions = {}
            substitutions['%user_link%'] = 'activate/' + user.profile_activation_key
            substitutions['%name%'] = user.company_name
            template = '55345630-06db-4987-863d-9189b0e97b57'

            # Send email welcome with activation link
            send_mail_template(user, template, substitutions)
            return Response(
                data={
                    'code': 200102,
                    'message': 'Email Sended',
                    'key': 'SEND_EMAIL_OK'
                },
                status=status.HTTP_200_OK
            )


class UpdatePassword(APIView):

    """
    API endpoint that allows to update user password.
    """

    def post(self, request, format=None):
        received = request.data
        user = request.user

        if ('current_password' in received.keys() and
                'new_password' in received.keys()):
            user = authenticate(
                username=user.username, password=received['current_password']
            )
            new_password = received['new_password']
            if user is not None:
                # the password verified for the user.
                if not _check_password(new_password):
                    return Response(
                        data={
                            'code': 400102,
                            'message': 'Password must be at least 6 chars long.',
                            'key': 'PASSWORD_WRONG'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        data={
                            'code': 200103,
                            'message': 'Password Updated',
                            'key': 'PASSWORD_UPDATE_OK'
                        },
                        status=status.HTTP_200_OK
                    )
            else:
                # Invalid current password.
                return Response(
                    data={
                        'code': 400112,
                        'message': 'Wrong current password.',
                        'key': 'CURRENT_PASSWORD_WRONG'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
                return Response(
                    data={
                        'code': 400113,
                        'message': 'current_password and new_password required.',
                        'key': 'REQUIRED_FIELDS'
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
