import pytest
from model_bakery import baker

from cooking_core.general.utils.cryptography import KeyPair


@pytest.fixture
def sender_key_pair():
    return KeyPair(
        public='eb01f474a637e402b44407f3c1044a0c4b59261515d50be9abd4ee34fcb9075b',
        private='acb34653559abebeabf67e01c89ab5f0859674c8a643b294b9ffc89012ac2e2e'
    )


@pytest.fixture
def sender_account_number(sender_key_pair):
    return sender_key_pair.public


@pytest.fixture
def sender_account(sender_account_number, db):
    return baker.make('accounts.Account', account_number=sender_account_number, balance=20000)
