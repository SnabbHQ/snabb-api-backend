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
from snabb.billing.views import ReceiptUserViewSet, ReceiptCourierViewSet


router = HybridRouter(trailing_slash=False)

# User related views
router.register(r'user/profile', ProfileViewSet)
router.add_api_view("user/register", url(r'^user/register',
                    RegisterUser.as_view(), name='register_user')),
router.add_api_view("user/verifyUser", url(r'^user/verifyUser',
                    VerifyUser.as_view(), name='verify_user')),
router.add_api_view("user/sendVerifyEmail", url(r'^user/sendVerifyEmail',
                    SendVerifyEmail.as_view(), name='send_verify_email'))
router.add_api_view("user/updatePassword", url(r'^user/updatePassword',
                    UpdatePassword.as_view(), name='update_password'))
router.add_api_view("user/forgotPassword", url(r'^user/forgotPassword',
                    ForgotPassword.as_view(), name='forgot_password'))
router.add_api_view("user/resetPassword", url(r'^user/resetPassword',
                    ResetPassword.as_view(), name='reset_password'))

# Address Views
router.add_api_view("address/validateAddress", url(r'^address/validateAddress',
                    ValidateAddress.as_view(), name='validateAddress'))

# Quote Views
router.register(r'deliveries/quote', QuoteViewSet, 'Quote')

# Order Views
router.register(r'billing/receiptUser', ReceiptUserViewSet, 'ReceiptUser')
router.register(r'billing/receiptCourier', ReceiptCourierViewSet, 'ReceiptCourier')
