from functools import partial
from typing import List

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from model_utils import FieldTracker

from cooking_core.accounts import consumers
from cooking_core.accounts.consumers import MessageType
from cooking_core.general.constants import ACCOUNT_NUMBER_LENGTH
from cooking_core.general.utils.misc import apply_on_commit
from cooking_core.general.validators import HexStringValidator

from ..managers.account import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    account_number = models.CharField(
        max_length=ACCOUNT_NUMBER_LENGTH, primary_key=True, validators=(HexStringValidator(ACCOUNT_NUMBER_LENGTH),)
    )
    balance = models.PositiveBigIntegerField(default=0)
    display_image = models.URLField(max_length=200, blank=True)
    display_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()
    tracker = FieldTracker()

    EMAIL_FIELD = None
    REQUIRED_FIELDS: List[str] = []
    USERNAME_FIELD = 'account_number'

    def __str__(self):
        return f'{self.account_number} | {self.balance}'

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def id(self):  # noqa: A003
        return self.account_number

    def save(self, *args, **kwargs):
        # Having `self.tracker.has_changed('balance')` prevents from sending events when an instance is saved with
        # the exact same value of balance (which is technically possible)
        if self.tracker.has_changed('balance') or self._state.adding:
            # TODO(dmu) MEDIUM: Consider always send an update notifications, but containing only those fields that
            #                   were updated
            # TODO(dmu) MEDIUM: Consider using serializer to create `message` if it gets more complex
            account_number = self.account_number
            message = {'account_number': account_number, 'balance': self.balance}
            apply_on_commit(
                # `consumers.send` so we can mock `send` in `consumers`
                partial(consumers.send, MessageType.UPDATE_ACCOUNT, account_number, message)
            )

        return super().save(*args, **kwargs)
