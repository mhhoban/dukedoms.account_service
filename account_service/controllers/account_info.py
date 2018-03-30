import json

import connexion
from flask import Flask, request
from flask_api import status
from account_service.shared.db import session
from account_service.models.account import Account

from swagger_server.models.account_info import (
    AccountInfo
)

def get_player_info(accountId):
    """
    endpoint for getting player account info
    """
    player_id = accountId

    try:
        account = retrieve_account_from_db(player_id)
        return populate_account_info(account), status.HTTP_200_OK
    except ValueError:
        return status.HTTP_404_NOT_FOUND

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

def retrieve_account_from_db(id):
    """
    lookup and return full account from db
    """
    account = session.query(Account).filter(Account.id == id).first()
    if account:
        return account
    else:
        raise ValueError

def populate_account_info(account):
    """
    populate swagger account info object with db account model data
    """
    account_info = AccountInfo(
        email=account.email,
        account_id=account.id,
        active_player_ids=account.active_player_ids,
        pending_player_ids=account.pending_player_ids,
        game_invitations=account.game_invitations
    )

    return account_info.to_dict()
