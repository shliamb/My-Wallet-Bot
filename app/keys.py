import os
from dotenv import load_dotenv
load_dotenv()


user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')