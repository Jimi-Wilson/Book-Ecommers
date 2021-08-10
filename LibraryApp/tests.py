from django.http import response
from django.test import TestCase, Client

# Create your tests here.


class TestURL(TestCase):
    def test_home_view(self):
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        request = self.client.get('')
