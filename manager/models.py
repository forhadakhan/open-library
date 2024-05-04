#manager/models.py 

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model representing a user in the system.

    Inherits from Django's AbstractUser model, providing additional
    fields and functionality for user management.

    Attributes:
        username: A unique identifier for the user.
        password: The user's password (stored in hashed form).
        email: The user's email address (required and unique).
        first_name: The user's first name.
        last_name: The user's last name.
        is_staff: A boolean indicating whether the user is a staff member.
        is_active: A boolean indicating whether the user's account is active.
        date_joined: The date and time when the user account was created.
    """

    email = models.EmailField(unique=True)  # Ensure email uniqueness

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Return a string representation of the user."""
        return self.username
