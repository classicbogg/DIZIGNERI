# DIZIGNERI / Sielom Backend

Django-бэкенд с админкой, API, регистрационной формой команды и экспортом в `.xlsx`.

## 1) Локальный запуск (приоритетный сценарий)

```bash
cd sielom
python3 -m venv .venv
source .venv/Scripts/activate           # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Проверка в браузере:
- `http://127.0.0.1:8000/` — главная (`index.html`)
- `http://127.0.0.1:8000/registration/` — регистрация (`registration.html`)
- `http://127.0.0.1:8000/health/` — healthcheck JSON
- `http://127.0.0.1:8000/admin/` — админка

## 2) Что уже интегрировано

- Шаблоны `index.html` и `registration.html` встроены в Django-роутинг.
- Шрифт `ONDER-REGULAR.TTF` подключен через Django static.
- Форма регистрации отправляет JSON на backend endpoint `/api/register-team`.
- На backend добавено сохранение заявки команды и 5 участников в БД.

## 3) Переменные окружения

См. `sielom/.env.example`.

Критичные для production:
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY=<сложный ключ>`
- `DJANGO_ALLOWED_HOSTS=sielom-web.online,www.sielom-web.online`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://sielom-web.online,https://www.sielom-web.online`
- `USE_SQLITE=0` (если PostgreSQL)

## 4) Production-подготовка (Ubuntu 24.04, без Docker)

### Установка на сервере
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql postgresql-contrib
```

### Деплой проекта
```bash
mkdir -p /home/pavel/apps
cd /home/pavel/apps
git clone <repo-url> DIZIGNERI
cd DIZIGNERI/sielom
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# отредактировать .env под production
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Systemd (gunicorn)
Готовый unit: `sielom/deploy/systemd/dizigneri.service`

```bash
sudo cp deploy/systemd/dizigneri.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dizigneri
sudo systemctl status dizigneri
```

### Nginx под отдельный домен
Готовый конфиг: `sielom/deploy/nginx/dizigneri.sielom-web.online.conf`

```bash
sudo cp deploy/nginx/dizigneri.sielom-web.online.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/dizigneri.sielom-web.online.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

> Важно: не удаляйте существующий `sites-enabled` конфиг для `sielom-web.ru`. Новый конфиг должен лежать отдельным файлом.

### SSL (Let’s Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d sielom-web.online -d www.sielom-web.online
```

## 5) Проверка после деплоя

```bash
curl -I http://sielom-web.online
curl -I https://sielom-web.online
curl https://sielom-web.online/health/
sudo systemctl status dizigneri
sudo systemctl status nginx
```

## 6) Docker-режим (опционально)

```bash
cd sielom
docker compose up --build -d
```

## 7) Тесты

```bash
python manage.py test
pytest -q
python manage.py check
```