from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import CustomUser

User = get_user_model()


class TestRegistrationViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-register')
        self.registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 1)

        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, self.registration_data['email'])

    def test_empty_data(self):
        response = self.client.post(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_username(self):
        registration_data = self.registration_data
        registration_data['username'] = ''

        response = self.client.post(self.url, data=registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exists_failure(self):
        # Test with invalid data to simulate a registration failure
        self.client.post(self.url, self.registration_data, format='json')
        response = self.client.post(self.url, self.registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_maching_passwords_failure(self):
        # Test with invalid data to simulate a registration failure upon not maching passwords
        registration_data = self.registration_data
        registration_data['password2'] = 'changed_password'

        response = self.client.post(self.url, registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_missing_second_password(self):
        registration_data = self.registration_data
        registration_data['password2'] = ''

        response = self.client.post(self.url, data=registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email(self):
        registration_data = self.registration_data
        registration_data['email'] = ''

        response = self.client.post(self.url, data=registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
