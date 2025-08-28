from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_upload_to(instance, filename):
    return f"profiles/{instance.username}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_upload_to, blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username

# Create your models here.
