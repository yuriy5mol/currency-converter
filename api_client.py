"""
API клиент для работы с курсами валют.
"""
import http_client
import storage
from typing import Any


FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]
MAX_AGE_HOURS = 24


def get_currency_rate(currency_code: str) -> dict[str, Any]: 
    """Получает курсы валют для указанной базовой валюты."""
    url = f"https://open.er-api.com/v6/latest/{currency_code}"    
    response = http_client.get(url)
    return response["json"]


def update_currency_rates() -> None:
    """Обновляет курсы валют для всех базовых валют."""
    all_data = {}
    for currency in FAVORITE_CURRENCIES:       
        all_data[currency] = get_currency_rate(currency)
    storage.save_to_file(all_data)


def read_currency_rates() -> dict[str, Any]:
    """Читает курсы валют из файла."""
    return storage.read_from_file()


def get_available_currencies() -> list[str]:
    """Возвращает список всех доступных валют."""
    rates_data = read_currency_rates()
    first_base = list(rates_data.keys())[0]
    return sorted(rates_data[first_base]["rates"].keys())


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Конвертирует сумму из одной валюты в другую."""
    rates_data = read_currency_rates()
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency not in rates_data:
        raise ValueError(f"Валюта {from_currency} не является базовой. Доступны: {list(rates_data.keys())}")
    
    if to_currency not in rates_data[from_currency]["rates"]:
        raise ValueError(f"Валюта {to_currency} не найдена")
    
    return amount * rates_data[from_currency]["rates"][to_currency]


def is_data_outdated() -> bool:
    """Проверяет, устарели ли данные (старше MAX_AGE_HOURS часов)."""
    if not storage.file_exists():
        return True
    return storage.get_file_age_hours() > MAX_AGE_HOURS