## Приложение на FastAPI с Postgres, docker-compose

Минимальный пример установки с помощью docker-compose, который
запускает базу данных postgres и веб-приложение FastAPI.

Веб-приложение FastAPI имеет одну конечную точку, которая:
* Вставляет строку в таблицу БД "приветствия", которая
  строковое представление текущей отметки времени.
* Возвращает список всех строк таблицы.


☝️ Цель этого репо — сделать тестовое задание для bewise.ai и показать в деле свои навыки.
В настройке postgres и FastAPI в docker-compose.
Старался, как можно лучше выполнить и ориентировался на лучшие практики.

## Running

Создайте и запустите как postgres, так и веб-приложение FastAPI:
```
docker compose up --build
```

Откройте корневую конечную точку по адресу http://localhost:8000/.

Откройте документацию API по адресу http://localhost:8000/redoc.

### Запуск только одного компонента
Чтобы запустить только базу данных:
```
docker compose up --build postgres
```

Чтобы запустить только веб-приложение FastAPI:
```
docker compose up --build app
```

## Проверка базы данных

Подключитесь к базе данных, открыв интерактивный сеанс для
докер-контейнер для базы данных:

```
docker compose exec postgres psql mydatabase --username myuser --password
или
./connect_db.sh
```
