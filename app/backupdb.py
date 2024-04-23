from keys import user_db, paswor_db
import subprocess
from datetime import datetime, timezone, timedelta
import asyncio
import logging

# Параметры подключения к базе данных PostgreSQL
db_username = user_db
db_password = paswor_db
db_name = "my_database"

backup_path = "./backup_db/"

async def backup_db():

    time_correction = +3 # Moscow
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=time_correction)
    current_datetime = a.strftime("%Y-%m-%d_%H-%M")
    backup_filename = f'{db_name}_backup_{current_datetime}.sql'

    # Формирование команды для создания резервной копии с помощью pg_dump
    #pg_dump_command = f'PGPASSWORD={db_password} pg_dump -h postgres -p 5432 -U {db_username} -d {db_name} -f {backup_path}{backup_filename}'
    pg_dump_command = f'PGPASSWORD={db_password} pg_dump -h localhost -p 5432 -U {db_username} -d {db_name} -F c -f {backup_path}{backup_filename}' # В бинарный формат


    try:
        subprocess.run(pg_dump_command, shell=True) # Выполнение команды через subprocess
        logging.info("Backup Data Base is Completed.")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Error when creating a backup: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(backup_db())

# Проверить когда буду запускать все в докере, тогда, при использовании постгреса докера, должен бекап работать