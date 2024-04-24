from worker_db import get_all_session, get_all_session_at_id, get_user_by_id, get_all_users_admin
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


# async def day_utcnow() -> datetime:
#     time_correction = +3 # Moscow
#     utc_zone = timezone.utc
#     a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
#     a = a + timedelta(hours=time_correction)
#     day_str = a.strftime("%Y-%m-%d_%H-%M")
#     # day = datetime.strptime(day_str, '%Y-%m-%d_%H-%M')
#     print(day_str)
#     #print("info: Getting the day and time from the server")
#     return day_str or None


# asyncio.run(day_utcnow())















async def ddf():
    data = await get_all_session()
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