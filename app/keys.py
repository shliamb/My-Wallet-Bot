from dotenv import load_dotenv
import os

user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')
telegram = os.environ.get('TELE_BOT')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))