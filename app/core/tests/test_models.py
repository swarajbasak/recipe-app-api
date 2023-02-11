"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_success(self):
        """Test creating a user with email successful"""
        email = 'test@example.com'
        password = 'pass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """Test email normalization"""
        emails = [
            ['abc@example.com', 'abc@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['test3@EXAMPLE.com', 'test3@example.com']
        ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_error(self):
        """Creating user without email raises value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '', 'pass123'
            )