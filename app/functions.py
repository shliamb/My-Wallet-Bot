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


# UNFORMAT TIME
async def unformat_date(date) -> str | int:
    day_now = str(date.strftime("%Y-%m-%d"))
    time_now = float(date.strftime("%H.%M"))
    return day_now, time_now


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

    m_wom = m_zap = m_site = m_chil = m_alim = m_cred = m_inv = m_hel = m_lich = m_subs = m_shuz = m_rest = m_shc = m_zdor = m_tra = m_com = m_inet = m_prod = m_bisnes = m_free = m_olds = m_rent  = m_invent = m_bonus = m_dolg = m_zp = 0
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
        y.append(round(m_wom, 2))
    if m_zap != 0:
        x.append(zap)
        y.append(round(m_zap, 2))
    if m_site != 0:
        x.append(site)
        y.append(round(m_site, 2))
    if m_chil != 0:
        x.append(chil)
        y.append(round(m_chil, 2))
    if m_alim != 0:
        x.append(alim)
        y.append(round(m_alim, 2))
    if m_cred != 0:
        x.append(cred)
        y.append(round(m_cred, 2))
    if m_inv != 0:
        x.append(inv)
        y.append(round(m_inv, 2))
    if m_hel != 0:
        x.append(hel)
        y.append(round(m_hel, 2))
    if m_lich != 0:
        x.append(lich)
        y.append(round(m_lich, 2))
    if m_subs != 0:
        x.append(subs)
        y.append(round(m_subs, 2))
    if m_shuz != 0:
        x.append(shuz)
        y.append(round(m_shuz, 2))
    if m_rest != 0:
        x.append(rest)
        y.append(round(m_rest, 2))
    if m_shc != 0:
        x.append(shc)
        y.append(round(m_shc, 2))
    if m_zdor != 0:
        x.append(zdor)
        y.append(round(m_zdor, 2))
    if m_tra != 0:
        x.append(tra)
        y.append(round(m_tra, 2))
    if m_com != 0:
        x.append(com)
        y.append(round(m_com, 2))
    if m_prod != 0:
        x.append(prod)
        y.append(round(m_prod, 2))
    if m_inet != 0:
        x.append(inet)
        y.append(round(m_inet, 2))
    if m_bisnes != 0:
        x.append(bisnes)
        y.append(round(m_bisnes, 2))
    if m_free != 0:
        x.append(free)
        y.append(round(m_free, 2))
    if m_olds != 0:
        x.append(olds)
        y.append(round(m_olds, 2))
    if m_rent != 0:
        x.append(rent)
        y.append(round(m_rent, 2))
    if m_zp != 0:
        x.append(zp)
        y.append(round(m_zp, 2))
    if m_dolg != 0:
        x.append(dolg)
        y.append(round(m_dolg, 2))
    if m_bonus != 0:
        x.append(bonus)
        y.append(round(m_bonus, 2))
    if m_invent != 0:
        x.append(invent)
        y.append(round(m_invent, 2))

    return x, y, name_month, name_year



















