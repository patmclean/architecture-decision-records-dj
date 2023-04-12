"""Tests for User model."""

from django.test import TestCase
from django.contrib.auth import get_user_model

TEST_AUTH_PWD = "098y7ty3fgv45nj!ki90u8yu"


class ModelTests(TestCase):
    """Test models."""

    def test_create_user(self):
        """Test creating a user with an email is successful."""
        username = "robouser"
        email = "robouser@example.ie"
        password = TEST_AUTH_PWD
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1", "test1@EXAMPLE.ie", "test1@example.ie"],
            ["test2", "Test2@Example.ie", "Test2@example.ie"],
            ["test3", "TEST3@EXAMPLE.ie", "TEST3@example.ie"],
            ["test4", "test4@example.IE", "test4@example.ie"],
        ]
        for username, email, expected in sample_emails:
            user = get_user_model().objects.create_user(username=username, email=email, password=TEST_AUTH_PWD)
            self.assertEqual(user.email, expected)

    def test_new_user_without_name_raises_error(self):
        """Test that creating a user without a name raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username="", password=TEST_AUTH_PWD)

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin_user = get_user_model().objects.create_superuser(
            username="super_user",
            email="super_user@example.ie",
            password=TEST_AUTH_PWD,
        )

        self.assertEqual(admin_user.username, "super_user")
        self.assertEqual(admin_user.email, "super_user@example.ie")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
