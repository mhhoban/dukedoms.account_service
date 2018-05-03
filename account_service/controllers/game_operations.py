import json
import logging

import connexion
from flask import Flask, request
from flask_api import status
from hamcrest import assert_that, equal_to

from account_service.shared.db import get_new_db_session
from account_service.models.account import Account
from sqlalchemy.exc import SQLAlchemyError
from account_service.exceptions.account_service_exceptions import (
    NoSuchAccountException
)
from account_service.controllers.account_info import (
    get_account_ids
)
from account_service.shared.account_operations import (
    check_account_id_exists,
    game_invite,
    retrieve_account_email,
    retrieve_account_id_from_db
)
from account_service.shared.oas_clients import game_service_client


logger = logging.getLogger('account_service_server')

def invite_accounts():
    """
    invite given accounts to a game of given id
    """
    requested_accounts = request.get_json()['invitedPlayers']
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

def process_game_invite():
    """
    take in game reply object, pass along appropriate response to game service
    """
    response_object = request.get_json()
    logger.debug(
        'received game invite response {} from player id {} for game_id {}'.format(
            response_object['accept'],
            response_object['accountId'],
            response_object['gameId']
        )
    )
    account_email = retrieve_account_email(response_object['accountId'])

    # TODO cleaner method for doing this
    session = get_new_db_session()
    account = session.query(Account).filter(Account.id == response_object['accountId']).first()

    if response_object['accept']:
        packet = send_invite_accept(
            game_id=response_object['gameId'],
            player_email=account_email,
            account_id=response_object['accountId']
        )

        pending_player_ids = json.loads(account.pending_player_ids)
        pending_player_ids['pending_player_ids'].append(packet.playerId)
        session.query(Account).filter(Account.id == response_object['accountId']).update(
            {'pending_player_ids': json.dumps(pending_player_ids)}
        )

        game_invites = json.loads(account.game_invitations)
        game_invites['game_invitation_ids'].remove(response_object['gameId'])
        session.query(Account).filter(Account.id == response_object['accountId']).update(
            {'game_invitations': json.dumps(game_invites)}
        )

        session.commit()
        session.close()
    else:
        send_invite_decline(
            game_id=response_object['gameId'],
            player_email=account_email,
            account_id=response_object['accountId']
        )
        game_invites = json.loads(account.game_invitations)
        game_invites['game_invitation_ids'].remove(response_object['gameId'])
        session.query(Account).filter(Account.id == response_object['accountId']).update(
            {'game_invitations': json.dumps(game_invites)}
        )

        session.commit()
        session.close()

    return None, status.HTTP_202_ACCEPTED

def send_invite_accept(game_id=None, player_email=None, account_id=None):
    """
    send player acceptance to game service and get welcome packet
    """
    result, status = game_service_client.gameOperations.accept_invite(
        gameInviteAcceptance={
            'gameId': game_id,
            'playerEmail': player_email,
            'accountId': account_id
        }
    ).result()
    return result

def send_invite_decline(game_id=None, player_email=None, account_id=None):
    """
    send player game rejection to game service
    """
    result, status = game_service_client.gameOperations.decline_invite(
        gameInviteRejection={
            'gameId': game_id,
            'playerEmail': player_email,
            'accountId': account_id
        }
    ).result()
