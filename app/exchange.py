import asyncio
import aiohttp
import xml.etree.ElementTree as ET # Pars XML
import logging


# Get exchange USD to RUB - переводит из доллара в рубли через XML Центробанка, так как все зарубежные не предоставляют о RUB, я не нашел бесплатно
# Получение стоимости 1$ 
async def get_exchange():
    try:
        usd = 1 # 1$ to RUB
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as response:
                data = await response.text()
        ex = (ET.fromstring(data).findtext('.//Valute[@ID="R01235"]/Value')) # значения валюты доллара США (USD) с помощью XPath выражения 
        ex = ex.replace(',', '.')  # Замена запятой на точку
        rub = float(usd) * float(ex)
        rub = round(rub, 2) # Округление до 2 цифр после запятой
        logging.info(f"Geting ex rate 1$ - {rub} Centrobank")
    except Exception as e:
        logging.error(f"Error geting exchange rate to url Centrobank")
        rub = None
    return rub or None  # Возврат стоимости одного $


# В базе есть таблица для курса, при расширении можно будет обновлять раз в день, для сокращения запросов




if __name__ == "__main__":
    asyncio.run(get_exchange())