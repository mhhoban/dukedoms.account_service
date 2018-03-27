import os

from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from account_service.constants import URLS

if os.environ.get('ACCOUNT_SERVICE_ENV') == 'local':
    env = 'local'
else:
    env= 'container'

engine = create_engine(URLS[env].rdbs)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property

@retry(wait_fixed=2000, stop_max_attempt_number=10)
def init_db():
    from account_service.models.account import Account
    Base.metadata.create_all(bind=engine)
