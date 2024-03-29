import os
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TKN')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD') or 'kege'
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_SCHEMA = 'ege'
DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Этапы/состояния разговора
FIRST, SECOND, THIRD, FOURTH, FIFTH = range(5)
# Данные обратного вызова
ONE, TWO, THREE, END, HELP = range(5)


LOG_FORMAT = '[%(levelname) -3s %(asctime)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
