# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from snabb.dispatching.webhooks import webhookTask
from .router_v1 import router


admin.autodiscover()

# REST Framework
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r"^payments/", include("pinax.stripe.urls")),
    url(regex=r'^task-webhook/',
        view=webhookTask, name='webhookTask'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
