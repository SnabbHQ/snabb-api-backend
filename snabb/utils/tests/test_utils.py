from django.test import TestCase
from snabb.utils.utils import get_app_info
from snabb.app_info.models import AppInfo


class UtilsTestCase(TestCase):
    def setUp(self):
        AppInfo.objects.create(name='dispatching_radius', content='3000')

    def test_get_dispatching_radius(self):
        radius = get_app_info('dispatching_radius', '6000')
        self.assertEqual(radius, '3000')
