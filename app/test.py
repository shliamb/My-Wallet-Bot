from worker_db import get_all_session, get_all_session_at_id, get_user_by_id
import asyncio







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








async def ddf():
    data = await get_all_session()
    for n in data:
        print(n.id)
        print(n.category)
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