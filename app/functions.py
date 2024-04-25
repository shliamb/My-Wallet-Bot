from datetime import datetime, timezone, timedelta
import asyncio
import re



# CHEC TEXT AND GET FLOAT
async def is_int_or_float(num):
    try:
        amount = float(num)
        return amount
    except ValueError:
        return None


# GET DAY AND TIME
async def day_utcnow() -> datetime:
    time_correction = +3 # Moscow
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=time_correction)
    day_str = a.strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
    print("info: Getting the day and time from the server")
    return day or None


# Регулярное выражение для поиска числа дня в формате YYYY-MM-DD взятого из базы
async def re_day(date_string):
    day_str = date_string.strftime("%Y-%m-%d %H:%M:%S")
    match = re.search(r'\d{4}-\d{2}-(\d{2})', day_str)
    if match:
        day = match.group(1)
        return day 


# Принимает дату из базы, достает номер месяца и сопостовляет название
async def re_month(date_db):
    day_str = date_db.strftime("%Y-%m-%d %H:%M:%S")
    match = re.search(r'\d{4}-(\d{2})-\d{2}', day_str)
    if match:
        day = int(match.group(1))

    if day == 1:
        month = "Январь"
    elif day == 2:
        month = "Февраль"
    elif day == 3:
        month = "Март"
    elif day == 4:
        month = "Апрель"
    elif day == 5:
        month = "Май"
    elif day == 6:
        month = "Июнь"
    elif day == 7:
        month = "Июль"
    elif day == 8:
        month = "Август"
    elif day == 9:
        month = "Сентябрь"
    elif day == 10:
        month = "Октябрь"
    elif day == 11:
        month = "Ноябрь"
    elif day == 12:
        month = "Декабрь"
    else:
        month = "Текущий месяц"
    return month 


# # UNFORMAT TIME
# async def unformat_date(date) -> str | int:
#     day_now = str(date.strftime("%Y-%m-%d"))
#     time_now = float(date.strftime("%H.%M"))
#     return day_now, time_now
















