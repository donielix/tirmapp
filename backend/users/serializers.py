from typing import Dict
from rest_framework import serializers
from .models import User, Address
from django.db import transaction
from rest_framework.validators import UniqueTogetherValidator


class AddressSerializer(serializers.ModelSerializer):
    tower = serializers.IntegerField()
    door = serializers.CharField(min_length=1, max_length=2)

    class Meta:
        model = Address
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Address.objects.all(), fields=["tower", "floor", "door"]
            )
        ]

    def validate_tower(self, value):
        """
        Validate tower value
        """
        VALID_VALUES = [1, 2, 3, 4, 5, 6]
        if value not in VALID_VALUES:
            raise serializers.ValidationError("`tower` value must be between 1 and 6.")
        return value


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "address", "password", "password2")
        extra_kwargs = {"email": {"required": True}}
    
    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError("Passwords must match")
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data: Dict):
        address_data: Dict = validated_data.pop("address")
        address_ser = AddressSerializer(data=address_data)
        address_ser.is_valid(raise_exception=True)
        address_obj: Address = address_ser.save()
        user_obj: User = User.objects.create(**validated_data, address=address_obj)
        return user_obj
