from keys import user_db, paswor_db
import subprocess
import asyncio
import logging

db_username = user_db
db_password = paswor_db
db_name = "my_database"
confirmation = False # На всякий случай подтверждение функции


async def restore_db(file_path):

    terminate_command = f'PGPASSWORD={db_password} psql -h postgres -p 5432 -U {db_username} -d {db_name} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=\'{db_name}\';"'

    clear_command = f'PGPASSWORD={db_password} psql -h postgres -p 5432 -U {db_username} -d {db_name} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'

    pg_restore_command = f'PGPASSWORD={db_password} pg_restore -h postgres -p 5432 -U {db_username} -d {db_name} {file_path}'
    
    try:
        subprocess.run(terminate_command, shell=True) # Формирование команды для завершения активных сеансов

        subprocess.run(clear_command, shell=True) # Формирование команды для удаления базы данных

        subprocess.run(pg_restore_command, shell=True) # Восстановления базы данных из резервной копии с помощью pg_restore, выполнение команды через subprocess
        
        confirmation = True
        logging.info("Database restore completed successfully.")
    except Exception as e:
        confirmation = False
        logging.info(f"An error occurred: {e}")

    return confirmation


if __name__ == "__main__":
    asyncio.run(restore_db())

