from datetime import datetime, timezone, timedelta
import asyncio



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

# # UNFORMAT TIME
# async def unformat_date(date) -> str | int:
#     day_now = str(date.strftime("%Y-%m-%d"))
#     time_now = float(date.strftime("%H.%M"))
#     return day_now, time_now
















