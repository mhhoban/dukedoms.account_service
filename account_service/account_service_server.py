import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from account_service.shared.db import session, init_db

app = connexion.App(__name__, specification_dir='swagger/')

app.add_api('account_service_api.yaml')
init_db()
app.run(port=5000)
