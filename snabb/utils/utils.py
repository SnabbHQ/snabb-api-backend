# encoding:utf-8
from rest_framework import pagination
from snabb.app_info.models import AppInfo


def get_app_info(value, defaultValue=None):
    try:
        resp = AppInfo.objects.get(name=value).content
    except AppInfo.DoesNotExist:
        resp = defaultValue
    return resp


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class FullResultsSetPagination(pagination.PageNumberPagination):
    page_size = 2000
    page_size_query_param = 'page_size'
    max_page_size = 10000
