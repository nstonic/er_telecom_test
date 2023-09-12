## Настройка

 - Для запуска сервиса понадобится python > 3.10
 - Создайте виртуальное окружение `python3 -m venv venv`
 - Запустите его `source venv/bin/activate`
 - Установите зависимости `pip install -r requirements.txt`
 - Задайте переменные окружения:
```shell
  SECRET_KEY = '123456'
  DEBUG = True
  ALLOWED_HOSTS = 127.0.0.1,localhost
```
- Отмигрируйте БД `python3 manage.py migrate`
- Запустите веб сервер `python3 manage.py runserver`

- Для проверки можно использовать тестовые данные из `test.json`