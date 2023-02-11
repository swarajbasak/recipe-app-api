"""Tests for user api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """helper for creating users"""
    return get_user_model().objects.create_user(**params)

def PublicUserAPITests(TestCase):
    """Public features of api"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test Creating user successful"""
        payload = {
            'email': 'example@example.com',
            'password': 'test123',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_user(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'example@example.com',
            'password': 'test123',
            'name': 'test name'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email': 'example@example.com',
            'password': 'tes',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        )

        self.assertFalse(user_exists)