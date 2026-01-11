"""
HTTP-клиент для выполнения запросов.
Модуль предоставляет базовые функции для GET и POST запросов.
"""

import requests
from typing import Any


class HTTPError(Exception):
    """Исключение для HTTP-ошибок."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


def get(url: str, params: dict | None = None, timeout: int = 10) -> dict[str, Any]:
    """
    Выполняет GET-запрос к указанному URL.
    
    Args:
        url: URL для запроса
        params: Параметры запроса (query string)
        timeout: Таймаут запроса в секундах
    
    Returns:
        Словарь с результатами: status_code, headers, body, json
    
    Raises:
        HTTPError: При статусе >= 400
        requests.exceptions.RequestException: При ошибках соединения
    """
    response = requests.get(url, params=params, timeout=timeout)
    
    result = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text,
        "json": None
    }
    
    # Пытаемся распарсить JSON
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            result["json"] = response.json()
        except ValueError:
            pass
    
    # Проверка статуса
    if response.status_code >= 400:
        raise HTTPError(response.status_code, response.text[:200])
    
    return result


def post(
    url: str,
    data: dict | None = None,
    json_data: dict | None = None,
    timeout: int = 10
) -> dict[str, Any]:
    """
    Выполняет POST-запрос к указанному URL.
    
    Args:
        url: URL для запроса
        data: Данные для отправки в формате form-data
        json_data: Данные для отправки в формате JSON
        timeout: Таймаут запроса в секундах
    
    Returns:
        Словарь с результатами: status_code, headers, body, json
    
    Raises:
        HTTPError: При статусе >= 400
        requests.exceptions.RequestException: При ошибках соединения
    """
    response = requests.post(url, data=data, json=json_data, timeout=timeout)
    
    result = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text,
        "json": None
    }
    
    # Пытаемся распарсить JSON
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            result["json"] = response.json()
        except ValueError:
            pass
    
    # Проверка статуса
    if response.status_code >= 400:
        raise HTTPError(response.status_code, response.text[:200])
    
    return result
