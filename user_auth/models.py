from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.username