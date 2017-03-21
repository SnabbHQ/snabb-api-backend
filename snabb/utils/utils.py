from snabb.app_info.models import AppInfo


def get_app_info(value, defaultValue=None):
    try:
        resp = AppInfo.objects.get(name=value).content
    except AppInfo.DoesNotExist:
        resp = defaultValue
    return resp
