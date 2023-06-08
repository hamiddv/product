from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .AccountMannager import AccountManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        max_length=128,
        primary_key=True
    )
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_verify_code = models.CharField(null=True, max_length=6)
    token = models.CharField(max_length=41, null=True, blank=True, default=None)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


