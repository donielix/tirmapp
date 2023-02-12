import getpass

from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand
from django.core.management.base import CommandError
from django.db import transaction
from users.models import Address, User


class Command(SuperUserCommand):
    help = "create super user with address"

    @transaction.atomic
    def handle(self, *args, **options):
        user = {
            "username": input("Username: "),
            "email": input("Email address:"),
            "password": getpass.getpass(),
            "password2": getpass.getpass("Password (again): "),
        }
        if user["password"] != user["password2"]:
            self.stderr.write("Error: Your passwords didn't match.")
            raise CommandError
        user.pop("password2")
        address = {
            "tower": input("Tower: "),
            "floor": input("Floor: "),
            "door": input("Door: "),
        }

        address = Address.objects.create(**address)
        user = User.objects.create(**user, address=address)
        user.is_staff = True
        user.is_superuser = True
        user.save()
