from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Last Name')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    is_organizer = models.BooleanField(default=False, verbose_name='Is Organizer')
    is_attendee = models.BooleanField(default=False, verbose_name='Is Attendee')
    is_staff = models.BooleanField(default=False, verbose_name='Is Staff')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        pass
