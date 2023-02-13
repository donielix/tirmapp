from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tower", "floor", "door"], name="unique_address")
        ]

    tower = models.SmallIntegerField()
    floor = models.SmallIntegerField()
    door = models.CharField(max_length=5)


class User(AbstractUser):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
