import json

import connexion
from flask import Flask, request
from flask_api import status
from account_service.shared.db import session
from account_service.models.account import Account

from swagger_server.models.new_account_request_successful import (
    NewAccountRequestSuccessful
)

def create_new_account():
    """
    endpoint for creating new account
    """
    account = request.get_json()
    account_email = account['email']
    new_account = Account(email=account_email)
    session.add(new_account)

    try:
        session.commit()
        response = NewAccountRequestSuccessful(
            email=account_email,
            account_id=new_account.id
        )
        return response.to_dict(), status.HTTP_200_OK

    except SQLAlchemyError:
        return status.HTTP_400_BAD_REQUEST
