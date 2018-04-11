import json
import logging

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from account_service.shared.db import init_db

logger = logging.getLogger('account_service_server')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('account_service.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

app = connexion.App(__name__, specification_dir='swagger/')

app.add_api('account_service_api.yaml')
init_db()
app.run(port=5000)
