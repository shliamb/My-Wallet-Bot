from datetime import datetime, timezone, timedelta
from exchange import get_exchange
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


# Регулярное выражение для поиска года в формате YYYY-MM-DD взятого из базы
async def re_year(date_string):
    date_str = date_string.strftime("%Y-%m-%d %H:%M:%S")
    match = re.search(r'(\d{4})-\d{2}-\d{2}', date_str)
    if match:
        year = match.group(1)
        return year 


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
        month = "месяц"
    return month 



# Собирает траты каждой категории если они есть по данным из DB за текущий месяц
async def sum_cat(flow, date_db):

    x = []
    y = []

    com = "Коммунальные услуги"
    prod = "Продукты питания"
    tra = "Транспорт"
    zdor = "Здравоохранение"
    shc = "Образование"
    rest = "Отдых и развлечения"
    shuz =  "Одежда и аксессуары"
    inet = "Связь и интернет"
    subs = "Платные подписки"
    lich = "Личная гигиена и уход"
    hel = "Подарки и благотворительность"
    inv = "Сбережения и инвестиции"
    cred = "Налоги и кредиты"
    alim = "Алименты"
    chil = "Покупки детям"
    site = "Хостинг, сайт, домены"
    zap = "Запчасти"
    wom = "Услуги противоположного пола"
    zp = "Заработная плата"
    dolg = "Долг, займы"
    bonus = "Премии и бонусы"
    invent = "Инвестиционный доход"
    rent = "Аренда жилья"
    olds = "Пенсия, пособия и социальные выплаты"
    free = "Фриланс и подработки"
    bisnes = "Бизнес"

    m_canc = m_wom = m_zap = m_site = m_cruj = m_chil = m_alim = m_cred = m_inv = m_hel = m_lich = m_subs = m_shuz = m_rest = m_shc = m_zdor = m_tra = m_com = m_are = m_inet = m_prod = m_stip = m_nasl = m_bisnes = m_free = m_vipl = m_comb = m_olds = m_rent  = m_invent = m_bonus = m_dolg = m_zp = m_are = 0
    i = 0


    for n in date_db:
        if i == 0:
            # Получение месяца 
            name_month = await re_month(n.date)
            name_year = await re_year(n.date)
                # Получение USD
            one_usdt = await get_exchange()
        
        if n.is_crypto is True:
            amount = float(n.amount) * one_usdt
        else:
            amount = float(n.amount)

        if n.flow == flow:
            if n.ml_category == prod:
                m_prod = m_prod + amount
            if n.ml_category == inet:
                m_inet = m_inet + amount
            if n.ml_category == com:
                m_com = m_com + amount
            if n.ml_category == tra:
                m_tra = m_tra + amount
            if n.ml_category == zdor:
                m_zdor = m_zdor + amount
            if n.ml_category == shc:
                m_shc = m_shc + amount
            if n.ml_category == rest:
                m_rest = m_rest + amount
            if n.ml_category == shuz:
                m_shuz = m_shuz + amount
            if n.ml_category == subs:
                m_subs = m_subs + amount
            if n.ml_category == lich:
                m_lich = m_lich + amount
            if n.ml_category == hel:
                m_hel = m_hel + amount
            if n.ml_category == inv:
                m_inv = m_inv + amount
            if n.ml_category == cred:
                m_cred = m_cred + amount
            if n.ml_category == alim:
                m_alim = m_alim + amount
            if n.ml_category == chil:
                m_chil = m_chil + amount
            if n.ml_category == site:
                m_site = m_site + amount
            if n.ml_category == zap:
                m_zap = m_zap + amount
            if n.ml_category == wom:
                m_wom = m_wom + amount
            if n.ml_category == zp:
                m_zp = m_zp + amount
            if n.ml_category == dolg:
                m_dolg = m_dolg + amount
            if n.ml_category == bonus:
                m_bonus = m_bonus + amount
            if n.ml_category == invent:
                m_invent = m_invent + amount
            if n.ml_category == rent:
                m_rent = m_rent + amount
            if n.ml_category == olds:
                m_olds = m_olds + amount
            if n.ml_category == free:
                m_free = m_free + amount
            if n.ml_category == bisnes:
                m_bisnes = m_bisnes + amount
        i += 1

    if m_wom != 0:
        x.append(wom)
        y.append(m_wom)
    if m_zap != 0:
        x.append(zap)
        y.append(m_zap)
    if m_site != 0:
        x.append(site)
        y.append(m_site)
    if m_chil != 0:
        x.append(chil)
        y.append(m_chil)
    if m_alim != 0:
        x.append(alim)
        y.append(m_alim)
    if m_cred != 0:
        x.append(cred)
        y.append(m_cred)
    if m_inv != 0:
        x.append(inv)
        y.append(m_inv)
    if m_hel != 0:
        x.append(hel)
        y.append(m_hel)
    if m_lich != 0:
        x.append(lich)
        y.append(m_lich)
    if m_subs != 0:
        x.append(subs)
        y.append(m_subs)
    if m_shuz != 0:
        x.append(shuz)
        y.append(m_shuz)
    if m_rest != 0:
        x.append(rest)
        y.append(m_rest)
    if m_shc != 0:
        x.append(shc)
        y.append(m_shc)
    if m_zdor != 0:
        x.append(zdor)
        y.append(m_zdor)
    if m_tra != 0:
        x.append(tra)
        y.append(m_tra)
    if m_com != 0:
        x.append(com)
        y.append(m_com)
    if m_prod != 0:
        x.append(prod)
        y.append(m_prod)
    if m_inet != 0:
        x.append(inet)
        y.append(m_inet)
    if m_bisnes != 0:
        x.append(bisnes)
        y.append(m_bisnes)
    if m_free != 0:
        x.append(free)
        y.append(m_free)
    if m_olds != 0:
        x.append(olds)
        y.append(m_olds)
    if m_rent != 0:
        x.append(rent)
        y.append(m_rent)
    if m_zp != 0:
        x.append(zp)
        y.append(m_zp)
    if m_dolg != 0:
        x.append(dolg)
        y.append(m_dolg)
    if m_bonus != 0:
        x.append(bonus)
        y.append(m_bonus)
    if m_invent != 0:
        x.append(invent)
        y.append(m_invent)

    return x, y, name_month, name_year










# # UNFORMAT TIME
# async def unformat_date(date) -> str | int:
#     day_now = str(date.strftime("%Y-%m-%d"))
#     time_now = float(date.strftime("%H.%M"))
#     return day_now, time_now
















