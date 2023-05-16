from rest_framework.exceptions import ValidationError

from cooking_core.accounts.models.account import Account
from cooking_core.config.models import get_value


def deduct_amount(*, account_number, amount):
    # It is crucial to make select_for_update(), so we get database row lock till the moment of actual update
    sender = Account.objects.select_for_update().get_or_none(account_number=account_number)
    sender.balance -= amount
    assert sender.balance >= 0
    sender.save()


def validate_balance_covers_transaction_fee(*, account_number):
    # It is crucial to make select_for_update(), so we get database row lock till the moment of actual update
    sender_account = Account.objects.select_for_update().get_or_none(account_number=account_number)
    if sender_account is None:
        raise ValidationError({'sender': ['Sender account does not exist']})

    if sender_account.balance < get_value('transaction_fee'):
        raise ValidationError({'amount': ['Transaction fee is greater than senders account balance']})
