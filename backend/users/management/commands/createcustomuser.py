import getpass

from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand
from django.core.management.base import CommandError
from django.db import transaction
from users.serializers import UserSerializer


class Command(SuperUserCommand):
    help = "create super user with address"

    def handle(self, *args, **options):
        user_data = {
            "username": input("Username: "),
            "email": input("Email address: "),
            "address": {
                "tower": input("Tower: "),
                "floor": input("Floor: "),
                "door": input("Door: "),
            },
            "password": getpass.getpass(),
            "password2": getpass.getpass("Password (again): "),
        }
        user = UserSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
