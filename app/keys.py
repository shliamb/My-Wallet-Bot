from dotenv import load_dotenv
import os
# # load_dotenv()


# # Укажите путь к вашему файлу .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# # Загрузите переменные окружения
load_dotenv(dotenv_path)

# # Теперь вы можете получить переменные окружения
user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')