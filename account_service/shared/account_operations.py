import json

from account_service.shared.db import get_new_db_session
from account_service.models.account import Account
from sqlalchemy.exc import SQLAlchemyError

from account_service.exceptions.account_service_exceptions import (
    NoSuchAccountException
)

def check_account_id_exists(account_id):
    """
    checks that given account id exists in db
    """
    session = get_new_db_session()

    try:
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            return True
        else:
            return False
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()

def retrieve_account_id_from_db(email):
    """
    lookup and return a given account id from the database
    """
    session = get_new_db_session()

    try:
        account = session.query(Account).filter(Account.email == email).first()
        if account:
            return account.id
        else:
            raise NoSuchAccountException
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()

def game_invite(account_id=None, game_id=None):
    """
    invites given account to given game
    Returns True if success, False if failure
    """
    session = get_new_db_session()

    try:
        account = session.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False

        game_invitations = json.loads(account.game_invitations)
        game_invitations['game_invitation_ids'].append(game_id)

        account.game_invitations = json.dumps(game_invitations)

        session.commit()

        return True
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()
