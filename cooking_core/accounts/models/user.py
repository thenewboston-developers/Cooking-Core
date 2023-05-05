from typing import List

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ..managers.user import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    account_number = models.CharField(max_length=64, primary_key=True)
    balance = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'account_number'
    EMAIL_FIELD = None
    REQUIRED_FIELDS: List[str] = []

    def __str__(self):
        return f'{self.account_number} | {self.balance}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def id(self):  # noqa: A003
        return self.account_number
