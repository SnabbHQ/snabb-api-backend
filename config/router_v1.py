# -*- coding: utf-8 -*-
from rest_framework import routers
from .hybridrouter import HybridRouter
from django.conf.urls import include, url
from snabb.users.views import (
    RegisterUser,
    VerifyUser,
    ProfileViewSet,
    SendVerifyEmail,
    UpdatePassword,
    ForgotPassword,
    ResetPassword
)
from snabb.address.views import ValidateAddress
from snabb.quote.views import QuoteViewSet

router = HybridRouter(trailing_slash=False)

# User related views
router.register(r'api/user/profile', ProfileViewSet)
router.add_api_view("api/user/register", url(r'^api/user/register',
                    RegisterUser.as_view(), name='register_user')),
router.add_api_view("api/user/verifyUser", url(r'^api/user/verifyUser',
                    VerifyUser.as_view(), name='verify_user')),
router.add_api_view("api/user/sendVerifyEmail", url(r'^api/user/sendVerifyEmail',
                    SendVerifyEmail.as_view(), name='send_verify_email'))
router.add_api_view("api/user/updatePassword", url(r'^api/user/updatePassword',
                    UpdatePassword.as_view(), name='update_password'))
router.add_api_view("api/user/forgotPassword", url(r'^api/user/forgotPassword',
                    ForgotPassword.as_view(), name='forgot_password'))
router.add_api_view("api/user/resetPassword", url(r'^api/user/resetPassword',
                    ResetPassword.as_view(), name='reset_password'))

# Address Views
router.add_api_view("api/address/validateAddress", url(r'^api/address/validateAddress',
                    ValidateAddress.as_view(), name='validateAddress'))

# Quote Views
router.register(r'api/quote/quote', QuoteViewSet, 'Quote')
