Flask API с двухуровневым кэшированием (Nginx + Redis)
запуск:
docker-compose up --build -d 
Проверка в браузере:
http://localhost/user/1 
1. Создание пользователя (POST)
curl -X POST -H "Content-Type: application/json" -d '{"username":"Sofia"}' http://localhost/user
2. Получение данных и проверка кэша (GET)
ввести:
curl.exe -i http://localhost/user/1
