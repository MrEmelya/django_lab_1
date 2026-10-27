from client import NewsAPIClient

# Замените на URL вашего локального сервера или адрес на Render
BASE_URL = "http://127.0.0.1:8000"

def main():
    print("--- Тестирование API ---")
    client = NewsAPIClient(BASE_URL)

    # 1. Регистрация
    print("\n1. Регистрация пользователя:")
    reg_response = client.register("testuser", "test@example.com", "StrongPassword123")
    print(reg_response)

    # 2. Авторизация (получение токена)
    print("\n2. Авторизация:")
    if client.login("testuser", "StrongPassword123"):
        print("Успешно вошли, токен получен.")
    else:
        print("Ошибка входа.")
        return

    # 3. Создание новости (контент должен быть > 50 символов из-за валидации)
    print("\n3. Создание новости:")
    content = "Это тестовый контент для новости, который должен быть длиннее пятидесяти символов, чтобы пройти валидацию."
    news = client.create_news("Тестовая новость из клиента", content, "Краткое описание")
    print(news)

    # 4. Получение списка новостей
    print("\n4. Список новостей:")
    news_list = client.get_news()
    print(f"Всего новостей: {news_list.get('count')}")
    if news_list.get('results'):
        print(f"Первая новость: {news_list['results'][0]['title']}")

    # 5. Обновление новости
    if news and 'id' in news:
        print(f"\n5. Обновление новости ID={news['id']}:")
        updated = client.update_news(news['id'], title="Обновленный заголовок")
        print(f"Новый заголовок: {updated.get('title')}")

        # 6. Удаление новости
        print(f"\n6. Удаление новости ID={news['id']}:")
        status = client.delete_news(news['id'])
        print(f"Статус ответа (204 = успех): {status}")

if __name__ == "__main__":
    main()
