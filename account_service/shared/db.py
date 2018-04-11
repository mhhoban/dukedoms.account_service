import os
import logging

from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from account_service.constants import URLS

logger = logging.getLogger('account_service_server')

if os.environ.get('ACCOUNT_SERVICE_ENV') == 'local':
    env = 'local'
else:
    env= 'container'

engine = create_engine(URLS[env].rdbs)
Base = declarative_base()


def get_new_db_session():
    """
    creates and returns a new session from the rdbs engine
    """
    return scoped_session(sessionmaker(bind=engine))

@retry(wait_fixed=2000, stop_max_attempt_number=10)
def init_db():
    from account_service.models.account import Account
    try:
        session = get_new_db_session()
        Base.query = session.query_property
        Base.metadata.create_all(bind=engine)
        logger.info('Created all models successfully')
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()
