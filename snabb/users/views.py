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
from django.conf import settings
from snabb.utils.code_response import get_response


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
                response = get_response(400101)
                return Response(data=response['data'], status=response['status'])

            if not _check_password(received['password']):
                response = get_response(400102)
                return Response(data=response['data'], status=response['status'])

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
                substitutions['%user_link%'] = settings.FRONTEND_URL+'activate/' + user.profile_activation_key
                substitutions['%name%'] = user.company_name
                template = '55345630-06db-4987-863d-9189b0e97b57'

                # Send email welcome with activation link
                send_mail_template(user, template, substitutions)

                serializer = ProfileSerializer(
                    user, context={'request': request}, partial=True)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            else:
                response = get_response(400103)
                return Response(data=response['data'], status=response['status'])
        else:
            response = get_response(400104)
            return Response(data=response['data'], status=response['status'])


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
            response = get_response(400105)
            return Response(data=response['data'], status=response['status'])

        try:
            user = Profile.objects.get(profile_activation_key=key)
        except Profile.DoesNotExist:
            response = get_response(400106)
            return Response(data=response['data'], status=response['status'])

        if user.verified:
            response = get_response(400107)
            return Response(data=response['data'], status=response['status'])

        if user.profile_activation_key == key and user.verified is False:
            user.verified = True
            user.save()

            response = get_response(200101)
            return Response(data=response['data'], status=response['status'])

        else:
            response = get_response(400108)
            return Response(data=response['data'], status=response['status'])


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
            response = get_response(400109)
            return Response(data=response['data'], status=response['status'])

        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            response = get_response(400110)
            return Response(data=response['data'], status=response['status'])

        if user.verified:
            response = get_response(400111)
            return Response(data=response['data'], status=response['status'])
        else:
            substitutions = {}
            substitutions['%user_link%'] = settings.FRONTEND_URL+'activate/' + user.profile_activation_key
            substitutions['%name%'] = user.company_name
            template = '55345630-06db-4987-863d-9189b0e97b57'

            # Send email welcome with activation link
            send_mail_template(user, template, substitutions)
            response = get_response(200102)
            return Response(data=response['data'], status=response['status'])


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
                    response = get_response(400102)
                    return Response(data=response['data'], status=response['status'])
                else:
                    user.set_password(new_password)
                    user.save()
                    response = get_response(200103)
                    return Response(data=response['data'], status=response['status'])
            else:
                # Invalid current password.
                response = get_response(400112)
                return Response(data=response['data'], status=response['status'])
        else:
            response = get_response(400113)
            return Response(data=response['data'], status=response['status'])


class ForgotPassword(APIView):

    """
    API endpoint that allows to send email for reset password.
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data

        if ('email' in received.keys()):
            email = received['email']
        else:
            response = get_response(400109)
            return Response(data=response['data'], status=response['status'])

        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            response = get_response(400110)
            return Response(data=response['data'], status=response['status'])

        #Create new hash for user:
        user.reset_password_key = "%s" % (uuid.uuid4(),)
        user.save()

        substitutions = {}
        substitutions['%user_link%'] = settings.FRONTEND_URL+'resetPassword/' + user.reset_password_key
        substitutions['%name%'] = user.company_name
        template = '50f0db97-ee40-4b23-859d-9e33f460eefd'
        # print(substitutions['%user_link%'])
        send_mail_template(user, template, substitutions)
        response = get_response(200102)
        return Response(data=response['data'], status=response['status'])


class ResetPassword(APIView):

    """
    API endpoint that allows to reset ther password.
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data

        if ('hash' in received.keys() and 'password' in received.keys()):
            key = received['hash']
            password = received['password']
        else:
            response = get_response(400114)
            return Response(data=response['data'], status=response['status'])

        try:
            user = Profile.objects.get(reset_password_key=key)
        except Profile.DoesNotExist:
            response = get_response(400106)
            return Response(data=response['data'], status=response['status'])

        user.password = password
        user.reset_password_key = ''
        user.save()
        response = get_response(200104)
        return Response(data=response['data'], status=response['status'])


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
