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

7 ДОМАШКА

сам Agro - https://localhost:8081/

сначала запустить ансибл плейбук из папки ansible чтобы поднять кластер:
ansible-playbook -i inventory.ini install_k3s.yml

после этого применить манифест для argocd, чтобы он подтянул чарты из гита:
kubectl apply -f argocd-auto-deploy.yaml

чтобы зайти в интерфейс арго (логин admin, пароль в секретах), пробросить порт:
kubectl port-forward svc/argocd-server -n argocd 8081:443

пароль узнать командой:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

само приложение будет доступно по nodeport:
http://localhost:30080
