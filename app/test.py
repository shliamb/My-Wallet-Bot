from worker_db import get_all_session, get_all_session_at_id, get_user_by_id, get_all_users_admin, get_session_by_month
import asyncio

















# async def ddf():

#     nn = await get_all_users_admin()
#     for n in nn:
#         if n:
#             print(n.id)
#             print(n.name)
#             print(n.full_name)
#             print(n.first_name)
#             print(n.last_name)
#             print(n.currency)
#             print(n.lang)
#             print(n.show_balance)
#             print(n.cash)
#             print(n.crypto)
#             print(n.crypto_currency)
#             print(n.cards)
#             print(n.is_admin)
#             print(n.is_block)
#             print(n.did_you_donate)
#             print(n.date)

#             print()



# asyncio.run(ddf())











































# async def ddf():
#     #id = 1666495
#     id = 6674458591
#     n = await get_user_by_id(id)
#     if n:
#         print(n.id)
#         print(n.name)
#         print(n.full_name)
#         print(n.first_name)
#         print(n.last_name)
#         print(n.currency)
#         print(n.lang)
#         print(n.show_balance)
#         print(n.cash)
#         print(n.crypto)
#         print(n.crypto_currency)
#         print(n.cards)
#         print(n.is_admin)
#         print(n.is_block)
#         print(n.did_you_donate)
#         print(n.date)

#         print()



# asyncio.run(ddf())





# from datetime import datetime, timezone, timedelta


async def ddf():

#     # time_correction = +3 # Moscow
#     # utc_zone = timezone.utc
#     # a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
#     # a = a + timedelta(hours=time_correction)
#     # # month = int(a.strftime("%m"))
#     # # year = int(a.strftime("%Y"))
#     # # day = int(a.strftime("%d"))

#     # day_str = a.strftime("%Y-%m-%d %H:%M:%S")
#     # day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')

#     #print(day)

#     #print(year, month, day)

#     # year = 2024
#     # month = 4

    id = 1666495

    data = await get_session_by_month(id)
    if data:
        for n in data:
            print(n.id)
            print(n.category)
            print(n.ml_category)
            print(n.flow)
            print(n.amount)
            print(n.is_cash)
            print(n.is_cards)
            print(n.is_crypto)
            print(n.date)
            print(n.users_id)
            print()



asyncio.run(ddf())













# from datetime import datetime, timezone, timedelta
# import re


# # time_correction = +3 # Moscow
# # utc_zone = timezone.utc
# # a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
# # a = a + timedelta(hours=time_correction)
# # day_str = a.strftime("%Y-%m-%d %H:%M:%S")


# # print(day_str)

# aa = "2024-12-25 22:37:52"

# # month = 4
# # name_month = await re_day(n.date)
# # print(month)

# async def re_month(date):
#     day_str = date.strftime("%Y-%m-%d %H:%M:%S")
#     match = re.search(r'\d{4}-(\d{2})-\d{2}', day_str)
#     if match:
#         day = int(match.group(1))

#     if day == 1:
#         month = "Январь"
#     elif day == 2:
#         month = "Февраль"
#     elif day == 3:
#         month = "Март"
#     elif day == 4:
#         month = "Апрель"
#     elif day == 5:
#         month = "Май"
#     elif day == 6:
#         month = "Июнь"
#     elif day == 7:
#         month = "Июль"
#     elif day == 8:
#         month = "Август"
#     elif day == 9:
#         month = "Сентябрь"
#     elif day == 10:
#         month = "Октябрь"
#     elif day == 11:
#         month = "Ноябрь"
#     elif day == 12:
#         month = "Декабрь"
#     else:
#         month = "Текущий месяц"
#     return month 

# asyncio.run(re_month(aa))
























# async def ddf():
#     data = await get_all_session()
#     for n in data:
#         print(n.id)
#         print(n.category)
#         print(n.ml_category)
#         print(n.flow)
#         print(n.amount)
#         print(n.is_cash)
#         print(n.is_cards)
#         print(n.is_crypto)
#         print(n.date)
#         print(n.users_id)
#         print()



# asyncio.run(ddf())























# id = 1666495
# async def ddf():
#     data = await get_all_session_at_id(id)
#     if data is None:
#         return
#     for n in data:
#         #print(n)
#         print(n.id)
#         print(n.category)
#         print(n.flow)
#         print(n.amount)
#         print(n.is_cash)
#         print(n.is_cards)
#         print(n.is_crypto)
#         print(n.date)
#         print(n.users_id)
#         print()



# asyncio.run(ddf())