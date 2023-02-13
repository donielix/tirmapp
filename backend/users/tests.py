import re
from collections import OrderedDict
from typing import Dict

from django.test import TestCase
from freezegun import freeze_time
from rest_framework.exceptions import ValidationError

from .models import Address, User
from .serializers import AddressSerializer, UserSerializer


class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "test-user",
            "email": "test@test.com",
            "address": {"tower": 1, "floor": 3, "door": "A"},
            "password": "test",
        }

    def assert_raises_validation_error(self, data: Dict, msg: str, ignore_case: bool = True):
        """
        Asserts that the given JSON data throws a `ValidationError` during DRF Serializer validation
        """
        if ignore_case:
            error = re.compile(msg, flags=re.I)
        else:
            error = re.compile(msg)
        user_ser = UserSerializer(data=data)
        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=error):
            user_ser.is_valid(raise_exception=True)

    @freeze_time("2020-01-01")
    def test_add_user_with_all_right_params(self):
        # De-serialization
        user_ser = UserSerializer(data=self.data)
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        # Serialization
        user_obj = UserSerializer(User.objects.get()).data
        address_obj = AddressSerializer(Address.objects.get()).data

        expected_user_obj = {
            "id": 1,
            "address": OrderedDict([("id", 1), ("tower", 1), ("floor", 3), ("door", "A")]),
            "password": "test",
            "last_login": None,
            "is_superuser": False,
            "username": "test-user",
            "first_name": "",
            "last_name": "",
            "email": "test@test.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2020-01-01T00:00:00Z",
            "groups": [],
            "user_permissions": [],
        }
        expected_address_obj = {"id": 1, "tower": 1, "floor": 3, "door": "A"}
        self.assertDictEqual(user_obj, expected_user_obj)
        self.assertDictEqual(address_obj, expected_address_obj)

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
