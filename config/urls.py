# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers
from .hybridrouter import HybridRouter
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

router = HybridRouter(trailing_slash=False)
router.register(
    r'api/user/profile',
    ProfileViewSet
)
router.add_api_view(
    "api/user/register",
    url(r'^api/user/register',
    RegisterUser.as_view(), name='register_user')
),
router.add_api_view(
    "api/user/verifyUser",
    url(r'^api/user/verifyUser',
    VerifyUser.as_view(), name='verify_user')
),
router.add_api_view(
    "api/user/sendVerifyEmail",
    url(r'^api/user/sendVerifyEmail',
    SendVerifyEmail.as_view(), name='send_verify_email')
)
router.add_api_view(
    "api/user/updatePassword",
    url(r'^api/user/updatePassword',
    UpdatePassword.as_view(), name='update_password')
)
router.add_api_view(
    "api/user/forgotPassword",
    url(r'^api/user/forgotPassword',
    ForgotPassword.as_view(), name='forgot_password')
)
router.add_api_view(
    "api/user/resetPassword",
    url(r'^api/user/resetPassword',
    ResetPassword.as_view(), name='reset_password')
)
router.add_api_view(
    "api/address/validateAddress",
    url(r'^api/address/validateAddress',
    ValidateAddress.as_view(), name='validateAddress')
)
admin.autodiscover()

urlpatterns = i18n_patterns(
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
)

# REST Framework
urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
