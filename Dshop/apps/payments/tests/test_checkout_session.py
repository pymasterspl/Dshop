from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase
from django.urls import reverse
from requests_mock import Mocker


class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_checkout_session(self):
        self.client.login(username='testuser', password='testpassword')

        with Mocker(json_encoder=DjangoJSONEncoder) as mocker:
            mocker.register_uri('POST', 'https://api.stripe.com/v1/checkout/sessions', json={'id': 'mocked_session_id'})

            response = self.client.get(reverse('create_checkout_session'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('sessionId', response.json())
