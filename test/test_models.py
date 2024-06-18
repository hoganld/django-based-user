from unittest import skipIf
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.test import TestCase

from .models import TestUser


def credentials():
    return "test@example.com", "excellence in testing"


class UserTest(TestCase):
    def setUp(self):
        self.email, self.password = credentials()

    def test_missing_password(self):
        user = TestUser(email=self.email, password="")
        with self.assertRaises(ValidationError):
            user.clean_fields()

    def test_missing_email(self):
        user = TestUser(email="", password=self.password)
        with self.assertRaises(ValidationError):
            user.clean_fields()

    def test_invalid_email(self):
        user = TestUser(email="username", password=self.password)
        with self.assertRaises(ValidationError):
            user.clean_fields()

    def test_default_not_staff(self):
        user = TestUser(email=self.email, password=self.password)
        self.assertFalse(user.is_staff)

    def test_default_active(self):
        user = TestUser(email=self.email, password=self.password)
        self.assertTrue(user.is_active)


class UserManagerTest(TestCase):

    def setUp(self):
        self.email, self.password = credentials()

    def test_create_default_user(self):
        user = TestUser.objects.create_user(email=self.email, password=self.password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_inactive_user(self):
        user = TestUser.objects.create_user(
            email=self.email, password=self.password, is_active=False
        )
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_staff_user(self):
        user = TestUser.objects.create_user(
            email=self.email, password=self.password, is_staff=True
        )
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = TestUser.objects.create_superuser(
            email=self.email, password=self.password
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserAuthenticationTest(TestCase):

    def setUp(self):
        self.email, self.password = credentials()
        self.user = TestUser.objects.create_user(
            email=self.email, password=self.password, is_active=True
        )

    def test_user_can_authenticate(self):
        user = authenticate(email=self.email, password=self.password)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user, self.user)

    def test_inactive_user_fails_authentication(self):
        self.user.is_active = False
        self.user.save()
        login = authenticate(email=self.email, password=self.password)
        self.assertIsNone(login)
