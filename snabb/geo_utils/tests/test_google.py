from django.test import TestCase
from snabb.geo_utils import google
from unittest.mock import patch


class GoogleTestCase(TestCase):

    @patch('google._private', return_value=2, autospec=True)
    def test_mock_not_private(self):
        a = google.not_private()
        self.assertEqual(a, 2)
