import json
import logging

from flask import request
from flask_api import status
from account_service.shared.db import get_new_db_session
from account_service.models.account import Account
from account_service.models.account_proxy import AccountProxy

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

    account_info_list = []
    for id in player_ids:
        account = AccountProxy(id)
        account_info_list.append(account.get_account_info())

    return account_info_list, status.HTTP_200_OK

def get_account_ids(requestedAccounts):
    """
    get player Id for given email addresses
    """
    requested_accounts = requestedAccounts
    logger.debug('received get_account_ids request for {}'.format(requested_accounts))
    try:
        account_mappings = (
            {'accountIdMappings':
                [{account:
                    retrieve_account_id_from_db(account)} for account in requested_accounts
                ]
            }
        )

        logger.debug('returning account id mappings {} for {}'.format(
            account_mappings,
            requested_accounts)
        )
        return account_mappings, status.HTTP_200_OK
    except NoSuchAccountException:
        logger.debug('unable to find requested account_ids')
        return status.HTTP_404_NOT_FOUND


def get_game_invites(accountId):
    """
    look up account, get game invites and return them
    """
    account_id = accountId
    logger.debug('received get_game_invites request for {}'.format(account_id))

    account = AccountProxy(account_id)

    return account.get_account_info()['gameInvitations'], status.HTTP_200_OK


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
        account.active_player_ids = json.loads(account.active_player_ids)
        account.pending_player_ids = json.loads(account.pending_player_ids)
        account.game_invitations = json.loads(account.game_invitations)
        logger.debug('found account for id {} in db'.format(id))

        return account
    except SQLAlchemyError:
        logger.error('unable to find account for id {} in db,'
                     'raising NoSuchAccountException'.format(id))
        raise NoSuchAccountException
    finally:
        session.close()
