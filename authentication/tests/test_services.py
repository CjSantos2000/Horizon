from django.contrib.auth.models import User
from django.test import TestCase

from ..services import create_user_as_admin


class TestServices(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(
            username="testuser", password="12345", is_superuser=True
        )
        self.user = User.objects.create_user(
            username="testuser1", password="12345", is_superuser=False
        )

    def test_create_user_as_admin_when_invalid(self):
        """Test create user service valid user and confirm_password."""
        with self.assertRaises(Exception):
            create_user_as_admin(
                username="testuser2",
                password="12345",
                email="test123123@gmail.com",
                user=self.user,
            )

    def test_create_user_as_admin_when_valid(self):
        """Test create user service valid"""
        user = create_user_as_admin(
            username="testuser2",
            password="Test12345.",
            email="testuser@gmail.com",
            user=self.user_admin,
        )
        self.assertEqual(user.username, "testuser2")
