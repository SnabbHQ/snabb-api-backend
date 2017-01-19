# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group, User
from .models import Profile
from .serializers import UserSerializer, GroupSerializer, ProfileSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
import uuid

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
            if current_user is False:
                user = Profile()
                user.email = received['email'].lower().replace(" ", "")
                user.password = received['password']
                user.phone = received['phone']

                if 'company_name' in received.keys():
                    user.company_name = received['company_name']

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
                        'code': 400105,
                        'message': 'Email already exists',
                        'key': 'EMAIL_ALREADY_EXISTS'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data={
                    'code': 400106,
                    'message': 'Company Name, Email, phone and password required',
                    'key': 'EMAIL_AND_PASSWORD_REQUIRED'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
