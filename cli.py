"""
Конвертер валют с консольным интерфейсом.
"""
import api_client
from http_client import HTTPError


def format_error(error: Exception) -> str:
    """Форматирует ошибку в читаемый вид."""
    if isinstance(error, HTTPError):
        messages = {
            404: "Ошибка подключения к API",
            500: "Ошибка сервера API. Попробуйте позже.",
            503: "Сервис временно недоступен. Попробуйте позже.",
        }
        return messages.get(error.status_code, f"Ошибка HTTP {error.status_code}")
    return str(error)


def check_and_update_if_needed() -> None:
    """Проверяет актуальность данных и уведомляет об автообновлении."""
    if api_client.is_data_outdated():
        print("⏳ Данные устарели. Обновляю курсы валют...")
        api_client.update_currency_rates()
        print("✅ Курсы обновлены!")


def wait_for_enter() -> None:
    """Ожидает нажатия Enter для продолжения."""
    input("\nНажмите Enter для продолжения...")


def print_currencies_list(currencies: list[str]) -> None:
    """Выводит список валют в 6 колонок."""
    cols = 6
    for i in range(0, len(currencies), cols):
        row = currencies[i:i + cols]
        print("  ".join(f"{c:<5}" for c in row))


def main_menu() -> None:
    """Главное меню программы."""
    print("\n" + "=" * 50)
    print("       💱 КОНВЕРТЕР ВАЛЮТ")
    print("=" * 50)
    print("\n1. Конвертировать валюту")
    print("2. Показать список доступных валют")
    print("3. Обновить курсы валют (запрос к API)")
    print("4. Показать курс валюты")
    print("0. Выход")
    print("-" * 50)


def show_exchange_rate() -> None:
    """Показывает курс выбранной валюты."""
    check_and_update_if_needed()
    from_cur = input("Базовая валюта (например, USD): ").strip().upper()
    to_cur = input("Целевая валюта (например, RUB): ").strip().upper()
    
    try:
        rate = api_client.convert_currency(1, from_cur, to_cur)
        print(f"\n📊 1 {from_cur} = {rate:.4f} {to_cur}")
    except ValueError as e:
        print(f"\n❌ Ошибка: {e}")
    except HTTPError as e:
        print(f"\n❌ {format_error(e)}")
    wait_for_enter()


def convert_interactive() -> None:
    """Интерактивная конвертация валюты."""
    check_and_update_if_needed()
    try:
        amount = float(input("Сумма для конвертации: "))
        from_cur = input("Из какой валюты (например, USD): ").strip().upper()
        to_cur = input("В какую валюту (например, RUB): ").strip().upper()
        
        result = api_client.convert_currency(amount, from_cur, to_cur)
        print(f"\n✅ {amount:,.2f} {from_cur} = {result:,.4f} {to_cur}")
        
    except ValueError as e:
        print(f"\n❌ Ошибка: {e}")
    except HTTPError as e:
        print(f"\n❌ {format_error(e)}")
    wait_for_enter()


def main() -> None:
    """Основная функция программы."""
    try:
        currencies = api_client.get_available_currencies()
        print(f"✅ Загружено из файла {len(currencies)} валют")
    except FileNotFoundError:
        print("⚠️ Файл с курсами не найден. Загружаю свежие данные...")
        api_client.update_currency_rates()
        currencies = api_client.get_available_currencies()
    
    while True:
        main_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            convert_interactive()
        
        elif choice == "2":
            print(f"\n📋 Доступные валюты ({len(currencies)} шт.):\n")
            print_currencies_list(currencies)
            wait_for_enter()
        
        elif choice == "3":
            print("\n⏳ Обновляю курсы валют...")
            try:
                api_client.update_currency_rates()
                currencies = api_client.get_available_currencies()
                print("✅ Курсы валют успешно обновлены!")
            except HTTPError as e:
                print(f"❌ {format_error(e)}")
            except Exception as e:
                print(f"❌ Ошибка обновления: {e}")
            wait_for_enter()
        
        elif choice == "4":
            show_exchange_rate()
        
        elif choice == "0":
            print("\n👋 До свидания!")
            break
        
        else:
            print("\n⚠️ Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
