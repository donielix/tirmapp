import re
from typing import Dict
from django.test import TestCase
from .serializers import UserSerializer
from .models import Address, User
from rest_framework.exceptions import ValidationError


class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "test-user",
            "email": "test@test.com",
            "address": {"tower": 1, "floor": 3, "door": "A"},
            "password": "test",
        }

    def assert_raises_validation_error(self, data: Dict, msg: str, ignore_case: bool = True):
        if ignore_case:
            error = re.compile(msg, flags=re.I)
        else:
            error = re.compile(msg)
        user_ser = UserSerializer(data=data)
        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=error):
            user_ser.is_valid(raise_exception=True)

    def test_add_user_with_all_right_params(self):
        user_ser = UserSerializer(data=self.data)
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        self.assertTrue(User.objects.exists())
        self.assertTrue(Address.objects.exists())

    def test_add_user_with_no_username(self):
        data = self.data.copy()
        data.pop("username")
        self.assert_raises_validation_error(data=data, msg="this field is required")

    def test_add_user_with_no_email(self):
        data = self.data.copy()
        data.pop("email")
        self.assert_raises_validation_error(data=data, msg="this field is required")

    def test_add_user_with_null_email(self):
        data = self.data.copy()
        data["email"] = None
        self.assert_raises_validation_error(data=data, msg="this field may not be null")

    def test_add_user_with_no_password(self):
        data = self.data.copy()
        data.pop("password")
        self.assert_raises_validation_error(data=data, msg="this field is required")

    def test_add_user_with_null_password(self):
        data = self.data.copy()
        data["password"] = None
        self.assert_raises_validation_error(data=data, msg="this field may not be null")

    def test_add_user_with_no_address(self):
        data = self.data.copy()
        data.pop("address")
        self.assert_raises_validation_error(data=data, msg="this field is required")

    def test_add_user_with_null_address(self):
        data = self.data.copy()
        data["address"] = None
        self.assert_raises_validation_error(data=data, msg="this field may not be null")

    def test_add_user_with_wrong_email(self):
        data = self.data.copy()
        data["email"] = "invalid-email"
        self.assert_raises_validation_error(data=data, msg="enter a valid email")
