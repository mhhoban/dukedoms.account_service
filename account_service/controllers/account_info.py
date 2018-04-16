import json
import logging

import connexion
from flask import Flask, request
from flask_api import status
from account_service.shared.db import get_new_db_session
from account_service.models.account import Account
from sqlalchemy.exc import SQLAlchemyError

from account_service.shared.account_operations import (
    retrieve_account_id_from_db
)
from account_service.exceptions.account_service_exceptions import (
    NoSuchAccountException
)
from swagger_server.models.account_info_list_player_accounts import AccountInfoListPlayerAccounts
from swagger_server.models.account_info_list import AccountInfoList
from swagger_server.models.unverified_players import UnverifiedPlayers


logger = logging.getLogger('account_service_server')

def get_player_info(accountIds):
    """
    endpoint for getting player account info
    """
    player_ids = accountIds
    logger.debug('received get_player_info request for {}'.format(player_ids))
    try:
        accounts = [
            populate_account_info(retrieve_account_from_db(player_id))
            for player_id in player_ids
        ]
        logger.debug('get_player_info returning account info {}'.format(accounts))
        return AccountInfoList(player_accounts=accounts).to_dict(), status.HTTP_200_OK
    except NoSuchAccountException:
        logger.debug('get_player_info unable for find account info')
        return None, status.HTTP_404_NOT_FOUND

def get_account_ids():
    """
    get player Id for given email addresses
    """
    requested_accounts = request.args.get('requestedAccounts').split(',')
    logger.debug('received get_account_ids request for {}'.format(requested_accounts))

    try:
        logger.debug('returning account id mappings for {}'.format(requested_accounts))
        return {'accountIdMappings':[{account: retrieve_account_id_from_db(account)} for account in requested_accounts]}, status.HTTP_200_OK
    except NoSuchAccountException:
        logger.debug('unable to find requested account_ids')
        return status.HTTP_404_NOT_FOUND


def verify_accounts():
    """
    return the player emails of accounts that do not exist in account service
    """
    requested_accounts = request.args.get('playerList').split(',')

    logger.debug('verify_accounts received request to verify {}'.format(requested_accounts))

    accounts_missing = []
    for account in requested_accounts:
        try:
            retrieved_account = retrieve_account_id_from_db(account)
        except NoSuchAccountException:
            accounts_missing.append(account)
    unverified_players = UnverifiedPlayers(unverified_players=accounts_missing)

    logger.debug(
        'verify_accounts returning {} unverified from {}'.format(
            requested_accounts,
            accounts_missing
            )
    )
    return unverified_players.to_dict(), status.HTTP_200_OK

def retrieve_account_from_db(id):
    """
    lookup and return full account from db
    """
    logger.debug('Trying to retreive account id {} from db'.format(id))
    try:
        session = get_new_db_session()
        account = session.query(Account).filter(Account.id == id).first()
        logger.debug('found account for id {} in db'.format(id))
        return account
    except SQLAlchemyError:
        logger.error('unable to find account for id {} in db,'
                     'raising NoSuchAccountException'.format(id))
        raise NoSuchAccountException
    finally:
        session.close()
def populate_account_info(account):
    """
    populate swagger account info object with db account model data
    """
    account_info = AccountInfoListPlayerAccounts(
        email=account.email,
        account_id=account.id,
        active_player_ids=account.active_player_ids,
        pending_player_ids=account.pending_player_ids,
        game_invitations=json.loads(account.game_invitations)
    )
    return account_info.to_dict()

def get_game_invites():
    pass
