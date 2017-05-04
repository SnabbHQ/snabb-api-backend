# encoding:utf-8
from rest_framework import pagination
from snabb.app_info.models import AppInfo


def get_app_info(value, defaultValue=None):
    try:
        resp = AppInfo.objects.get(name=value).content
    except AppInfo.DoesNotExist:
        resp = defaultValue
    return resp


def get_delivery_from_task(task):
    from snabb.quote.models import Quote
    from snabb.deliveries.models import Delivery
    quote = Quote.objects.filter(tasks=task)
    # If more than one quote, or quote doesn't exists, doesn't return delivery.
    if quote.count() != 1:
        return None
    else:
        try:
            delivery = Delivery.objects.get(delivery_quote=quote[:1])
            return delivery
        except Delivery.DoesNotExist:
            return None


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class FullResultsSetPagination(pagination.PageNumberPagination):
    page_size = 2000
    page_size_query_param = 'page_size'
    max_page_size = 10000
