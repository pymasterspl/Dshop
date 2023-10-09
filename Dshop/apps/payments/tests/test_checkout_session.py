from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_checkout_session(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_checkout_session'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sessionId', response.json())
