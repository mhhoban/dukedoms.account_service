import json
import logging

import connexion
from flask import Flask, request
from flask_api import status

from account_service.shared.db import get_new_db_session
from account_service.models.account import Account
from sqlalchemy.exc import SQLAlchemyError
from account_service.exceptions.account_service_exceptions import (
    NoSuchAccountException
)
from account_service.shared.account_operations import (
    check_account_id_exists,
    game_invite,
    retrieve_account_id_from_db
)


logger = logging.getLogger('account_service_server')

def invite_accounts():
    """
    invite given accounts to a game of given id
    """
    requested_accounts = request.get_json()['playerList']
    game_id = request.get_json()['gameId']
    logger.debug(
        'invite_accounts received request to invite players {} to game)id {}'.format(
            requested_accounts,
            game_id
        )
    )

    requested_accounts = [retrieve_account_id_from_db(account) for account in requested_accounts]

    for account_id in requested_accounts:
        if not game_invite(account_id=account_id, game_id=game_id):
            logger.error(
                'tried to invite player id {} to game id{} but player does not exist'.format(
                    account_id,
                    game_id
                )
            )
            return None, status.HTTP_500_INTERNAL_SERVER_ERROR
    logger.debug(
        'successfully invited players {} to game_id {}'.format(
            requested_accounts,
            game_id
        )
    )
    return None, status.HTTP_202_ACCEPTED
