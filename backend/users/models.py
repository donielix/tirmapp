from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)


class Address(models.Model):
    class Meta:
        indexes = [models.Index(fields=["tower", "floor", "door"], name="address_idx")]
        constraints = [
            models.CheckConstraint(
                check=models.Q(tower__in=[1, 2, 3, 4, 5, 6]), name="tower_values"
            ),
            models.CheckConstraint(check=models.Q(door__length__gt=0), name="door_min_length"),
            models.UniqueConstraint(fields=["tower", "floor", "door"], name="unique_address"),
        ]

    tower = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    door = models.CharField(max_length=2)


class User(AbstractUser):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
