Запуск
docker-compose up --build -d
Миграции
Применить существующие миграции:
docker-compose exec backend flask db upgrade
Основные эндпоинты (CRUD)
1. Создание пользователя (POST)
curl.exe -X POST -H "Content-Type: application/json" -d '{\"username\":\"Sofia\"}' http://localhost/user
2. Получение данных и проверка кэша (GET)
Первый запрос идет в БД, последующие — в кэш (Redis/Nginx).
curl.exe -i http://localhost/user/1
3. Обновление данных (PUT)
При обновлении кэш автоматически сбрасывается.
curl.exe -X PUT -H "Content-Type: application/json" -d '{\"username\":\"Sofia_Updated\"}' http://localhost/user/1
4. Удаление пользователя (DELETE)
Удаляет запись из БД и очищает кэш.
curl.exe -X DELETE http://localhost/user/1
