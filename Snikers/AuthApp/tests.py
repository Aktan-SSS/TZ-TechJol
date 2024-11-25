from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterViewTest(APITestCase):
    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'password123',
            'password_confirm': 'different_password',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Пароли не совпали')

    def test_register_user_username_taken(self):
        User.objects.create_user(username='testuser', password='password123')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Имя пользователя уже занято', response.data['non_field_errors'][0])
