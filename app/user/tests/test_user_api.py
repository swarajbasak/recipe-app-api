"""Tests for user api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

    def test_create_token_for_user(self):
        """Creates tokeb for valid credentials"""
        user_details = {
            'name': 'test name',
            'email': 'test@example.com',
            'password': 'pass123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error for bad password"""
        user_details = {
            'name': 'test name',
            'email': 'test@example.com',
            'password': 'goodpass'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'badpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_bad_password(self):

        payload = {
            'email': 'email@eg.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserAPITest(TestCase):
    """Test API requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='user@example.com',
            password='test1234',
            name='test name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def RetrieveProfileSuccess(self):
        """Test retrieving profile for authenticated user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email
        })

    def test_post_me_url_not_allowed(self):
        """Test POST is not allowed for me url"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'name':'updated name',
            'password': 'newpass'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


