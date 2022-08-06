# API случайных слов

Возвращает список случайных слов в виде `json`.
Слова могут быть на русском или английском языке в зависимости от параметра `language`. Допустимые значения:

- `ru` - русский
- `eng` - английский

Количество слов можно изменить с помощью параметра `quantity`. Не должен быть меньше 0.

## Запуск приложения

### Docker

Проект имеет `Dockerfile` и `docker-compose` файлы. Чтобы запустить на `8080` порту введите следующую команду:

```
$ docker-compose up
```

### Виртуальное окружение
Создадим и активируем виртуальное окружение:
```
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements/dev.txt
```
Запускаем сервер на `8080` порту:
```
$ python random_words/manage.py 8080
```
## Запросы/ответы
```
$ curl http://127.0.0.1:8080/words/?quantity=5
{
    "language": "ru",
    "quantity": 5,
    "words": [
        "форма",
        "проговорить",
        "устройство",
        "могучий",
        "холм"
    ]
}
```

```
$ curl 'http://127.0.0.1:8080/words/?quantity=2&language=eng'
{
    "language": "eng",
    "quantity": 2,
    "words": [
        "agenda",
        "balance"
    ]
}
```

```
$ curl http://127.0.0.1:8080/words/?language=pol
{
    "status_code": 400,
    "detail": "Неизвестный язык `pol`"
}
```

```
$ curl http://127.0.0.1:8080/words/?quantity=-2
{
    "status_code": 400,
    "detail": "Количество слов не может быть меньше нуля."
}
```
