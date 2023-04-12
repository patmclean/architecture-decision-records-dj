"""App Models for User."""

from django.contrib.auth.models import AbstractUser

# from django.db import models


class User(AbstractUser):
    """Application User model to override default django model."""

    pass
