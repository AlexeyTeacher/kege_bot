import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.ddl import CreateSchema

from config import DB_SCHEMA, LOG_FORMAT, DB_URL
from models import metadata_obj, Base

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger('app')

ENGINE = create_engine(DB_URL, pool_pre_ping=True)

logger.info(f'{ENGINE=}')


def db_init():
    try:
        logger.info('try to create schemas')
        ENGINE.execute(CreateSchema(DB_SCHEMA))
    except ProgrammingError as err:
        logger.error(f'{err=}')
        pass
    metadata_obj.create_all(ENGINE)


Base.metadata.bind = ENGINE
session = scoped_session(sessionmaker(bind=ENGINE))
