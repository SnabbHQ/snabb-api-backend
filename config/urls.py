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

from snabb.deliveries.views import DeliveriesViewSet, QuotesViewSet
from snabb.users.views import RegisterUser, VerifyUser, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'deliveries', DeliveriesViewSet)
router.register(r'quotes', QuotesViewSet)
router.register(r'api/user/profile', ProfileViewSet)
admin.autodiscover()

urlpatterns = i18n_patterns(
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
)

# REST Framework
urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/user/register', RegisterUser.as_view(), name='register_user'),
    url(r'^api/user/verifyUser', VerifyUser.as_view(), name='verify_user'),
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
