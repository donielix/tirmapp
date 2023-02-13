from typing import Dict
from rest_framework import serializers
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data: Dict):
        address_data: Dict = validated_data.pop("address")
        address_ser = AddressSerializer(data=address_data)
        address_ser.is_valid(raise_exception=True)
        address_obj: Address = address_ser.save()
        user_obj: User = User.objects.create(**validated_data, address=address_obj)
        return user_obj
