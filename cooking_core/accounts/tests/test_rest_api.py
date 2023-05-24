def test_retrieve_account(sender_account, api_client):
    response = api_client.get(f'/api/accounts/{sender_account.account_number}')
    assert response.status_code == 200
    assert response.json() == {
        'account_number': sender_account.account_number,
        'balance': sender_account.balance,
        'display_image': '',
        'display_name': '',
    }
