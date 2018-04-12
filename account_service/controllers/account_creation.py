import json
import logging

import connexion
from flask import Flask, request
from flask_api import status
from account_service.shared.db import get_new_db_session
from account_service.models.account import Account

from swagger_server.models.new_account_request_successful import (
    NewAccountRequestSuccessful
)

logger = logging.getLogger('account_service_server')

def create_new_account():
    """
    endpoint for creating new account
    """
    account = request.get_json()
    account_email = account['email']
    logger.debug(
        'create_new_account received request to create account for email {}'.format(
            account_email
        )
    )
    new_account = Account(email=account_email)
    session = get_new_db_session()
    session.add(new_account)

    try:
        session.commit()
        response = NewAccountRequestSuccessful(
            email=account_email,
            account_id=new_account.id
        )
        logger.debug(
            'succesfully created new account id {} for email {}'.format(
                new_account.id,
                account_email
            )
        )
        return response.to_dict(), status.HTTP_200_OK

    except SQLAlchemyError:
        logger.error(
            'SQLAlchemyError while trying to create ne account for {}'.format(
                account_email
            )
        )
        return status.HTTP_400_BAD_REQUEST
    finally:
        session.close()
