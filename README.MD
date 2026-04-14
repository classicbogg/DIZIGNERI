# DIZIGNERI / Sielom Backend

Django-бэкенд с админкой, API и экспортом в `.xlsx`.

## Быстрый старт (Windows Git Bash)

```bash
cd sielom
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Открывать только: `http://127.0.0.1:8000/`.

## Если видите в консоли “You're accessing the development server over HTTPS”

Это **не падение Django**. На `runserver` кто-то стучится HTTPS-трафиком (браузер, расширение, антивирус или HSTS), а dev-сервер умеет только HTTP.

Что делать:
1. В адресной строке вводить только `http://127.0.0.1:8000/`.
2. Проверить, что браузер не автозаменяет на `https://`.
3. Открыть в инкогнито/другом браузере.

## Если `createsuperuser` пишет “username already taken”

Пользователь уже существует. Используйте другой username **или** поменяйте пароль:

```bash
python manage.py changepassword Admin
```

## Тесты (правильные команды)

```bash
# Django tests
python manage.py test

# Pytest напрямую
pytest -q

# Или через алиас команды Django
python manage.py pytest
```

## PostgreSQL режим

Локально по умолчанию SQLite (чтобы запускалось сразу).
Для PostgreSQL в `.env`:

```env
USE_SQLITE=0
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sielom
DB_USER=sielom
DB_PASSWORD=sielom
DB_HOST=127.0.0.1
DB_PORT=5432
```

Если PostgreSQL локально не настроен — используйте Docker:

```bash
docker compose up --build
```

## Экспорт в Excel

`/admin/` → `Records` → кнопка **Экспорт в XLSX**.
Файл: `records_export.xlsx`.

## Продакшен для sielom-web.online

- Nginx: `sielom/deploy/nginx/sielom-web.online.conf`
- Docker: `sielom/Dockerfile`, `sielom/docker-compose.yml`
- CI: `.github/workflows/ci.yml`