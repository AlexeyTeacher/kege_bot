import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TKN')
API_HOST = os.getenv('API_HOST')