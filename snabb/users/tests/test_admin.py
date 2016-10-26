from test_plus.test import TestCase


class TestMyUserCreationForm(TestCase):

    def setUp(self):
        self.user = self.make_user()
