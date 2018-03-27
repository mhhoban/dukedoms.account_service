import json

import connexion
from flask import Flask, request
from flask_api import status
from account_service.shared.db import session
from account_service.models.account import Account

def get_player_info():
    """
    endpoint for getting player account info
    """
    player_id = request.json()['playerId']


def get_account_ids():
    """
    get player Id for given email address
    """
    requested_accounts = requests.json()['requestedAccounts']

    try:
        return [{account: retrieve_account_id_from_db(account)} for account in account], status.HTTP_200_OK
    except ValueError:
        return status.HTTP_404_NOT_FOUND


def verify_accounts():
    pass

def retrieve_account_id_from_db(email):
    """
    lookup and return a given account id from the database
    """
    account = session.query(Account).filter(Account.email == email).first()
    if account:
        return account.id
    else:
        raise ValueError
