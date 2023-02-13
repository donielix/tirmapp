import re
from django.test import TestCase
from .serializers import UserSerializer
from .models import Address, User
from rest_framework.exceptions import ValidationError


class TestUserSerializer(TestCase):
    def test_add_user_with_all_right_params(self):
        data = {
            "username": "test-user",
            "email": "test@test.com",
            "address": {"tower": 1, "floor": 3, "door": "A"},
            "password": "test",
        }
        user_ser = UserSerializer(data=data)
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        self.assertTrue(User.objects.exists())
        self.assertTrue(Address.objects.exists())

    def test_add_user_with_wrong_email(self):
        data = {
            "username": "test-user",
            "email": "invalid_email",
            "address": {"tower": 1, "floor": 3, "door": "A"},
            "password": "test",
        }
        user_ser = UserSerializer(data=data)
        error = re.compile("enter a valid email", flags=re.I)
        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=error):
            user_ser.is_valid(raise_exception=True)
