# Развёртывание на сервере (Ubuntu / Debian)

## Часть 1: Подготовка сервера

### Шаг 1.1: Подключитесь к серверу по SSH

**Windows (PowerShell или PuTTY):**
```powershell
ssh root@YOUR_SERVER_IP
```

**Mac/Linux:**
```bash
ssh root@YOUR_SERVER_IP
```

Замените `YOUR_SERVER_IP` на IP-адрес вашего сервера.

Введите пароль, когда попросят.

### Шаг 1.2: Обновите систему

```bash
apt update && apt upgrade -y
```

Ждите окончания обновления (может занять 5-10 минут).

---

## Часть 2: Установка необходимых программ

### Шаг 2.1: Установите Python и зависимости

```bash
apt install python3 python3-pip python3-venv python3-dev -y
```

### Шаг 2.2: Установите базу данных SQLite (входит в состав Python)

SQLite уже включён в Python, дополнительная установка не требуется.

### Шаг 2.3: Установите Nginx

```bash
apt install nginx -y
```

### Шаг 2.4: Установите Git

```bash
apt install git -y
```

### Шаг 2.5: Установите Supervisor (для автозапуска)

```bash
apt install supervisor -y
```

### Шаг 2.6: Проверьте установку

```bash
python3 --version
nginx -v
```

Должны показать версии.

---

## Часть 3: Создание пользователя для проекта

### Шаг 3.1: Создайте пользователя

```bash
useradd -m -s /bin/bash altersert
```

### Шаг 3.2: Добавьте пользователя в группу sudo

```bash
usermod -aG sudo altersert
```

### Шаг 3.3: Установите пароль для пользователя

```bash
passwd altersert
```

Введите пароль дважды.

### Шаг 3.4: Переключитесь на нового пользователя

```bash
su - altersert
```

Теперь вы работаете от имени пользователя `altersert`.

---

## Часть 4: Загрузка проекта

### Шаг 4.1: Перейдите в домашнюю папку

```bash
cd ~
```

### Шаг 4.2: Загрузите проект

**Вариант A: Через Git**
```bash
git clone https://github.com/yourusername/altersert_django.git
```

**Вариант B: Через SCP (с вашего компьютера)**

На вашем компьютере выполните:
```bash
scp -r /path/to/altersert_django altersert@YOUR_SERVER_IP:~/
```

**Вариант C: Через ZIP-архив**

Загрузите архив на сервер, затем:
```bash
unzip altersert_django.zip
```

### Шаг 4.3: Перейдите в папку проекта

```bash
cd ~/altersert_django
```

---

## Часть 5: Настройка виртуального окружения

### Шаг 5.1: Создайте виртуальное окружение

```bash
python3 -m venv venv
```

### Шаг 5.2: Активируйте виртуальное окружение

```bash
source venv/bin/activate
```

Должно появиться `(venv)` в начале строки.

### Шаг 5.3: Обновите pip

```bash
pip install --upgrade pip
```

### Шаг 5.4: Установите зависимости

```bash
pip install -r requirements.txt
```

Ждите окончания установки.

---

## Часть 6: Настройка проекта

### Шаг 6.1: Создайте файл .env

```bash
nano .env
```

### Шаг 6.2: Вставьте содержимое в .env

Удалите всё (Ctrl+K удаляет строку) и вставьте:

```env
# Django Settings
DEBUG=False
SECRET_KEY=замените-это-на-случайную-строку-из-50-символов
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_SERVER_IP

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Telegram Bot Settings (опционально)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=ваш-сложный-пароль-здесь
ADMIN_EMAIL=admin@your-domain.com
```

**ВАЖНО:**
- Замените `your-domain.com` на ваш реальный домен
- Замените `YOUR_SERVER_IP` на IP сервера
- Сгенерируйте SECRET_KEY:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(50))"
  ```
- Придумайте сложный пароль для админа

### Шаг 6.3: Сохраните файл

Нажмите:
- `Ctrl+O` (сохранить)
- `Enter` (подтвердить)
- `Ctrl+X` (выйти)

### Шаг 6.4: Примените миграции

```bash
python manage.py migrate
```

### Шаг 6.5: Создайте суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: ваш email
- Password: сложный пароль
- Password (again): повторите пароль

### Шаг 6.6: Загрузите начальные данные

```bash
python manage.py init_data
```

### Шаг 6.7: Соберите статические файлы

```bash
python manage.py collectstatic --noinput
```

---

## Часть 7: Настройка Gunicorn

### Шаг 7.1: Установите Gunicorn

```bash
pip install gunicorn
```

### Шаг 7.2: Проверьте запуск Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 altersert.wsgi:application
```

Откройте в браузере: `http://YOUR_SERVER_IP:8000/`

Должен открыться сайт.

Остановите Gunicorn (Ctrl+C).

### Шаг 7.3: Создайте конфигурацию Supervisor

Выйдите из пользователя altersert:
```bash
exit
```

Теперь вы снова root.

Создайте файл конфигурации:
```bash
nano /etc/supervisor/conf.d/altersert.conf
```

Вставьте:

```ini
[program:altersert]
command=/home/altersert/altersert_django/venv/bin/gunicorn --workers 3 --bind unix:/home/altersert/altersert_django/app.sock altersert.wsgi:application
user=altersert
group=www-data
working_directory=/home/altersert/altersert_django
autostart=true
autorestart=true
redirect_stderr=true
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 7.4: Перезапустите Supervisor

```bash
supervisorctl reread
supervisorctl update
supervisorctl start altersert
```

### Шаг 7.5: Проверьте статус

```bash
supervisorctl status
```

Должно показать:
```
altersert RUNNING
```

---

## Часть 8: Настройка Nginx

### Шаг 8.1: Удалите дефолтный конфиг

```bash
rm /etc/nginx/sites-enabled/default
```

### Шаг 8.2: Создайте конфиг для вашего сайта

```bash
nano /etc/nginx/sites-available/altersert
```

Вставьте (замените `your-domain.com` на ваш домен):

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/altersert/altersert_django;
    }

    location /media/ {
        root /home/altersert/altersert_django;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/altersert/altersert_django/app.sock;
    }
}
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 8.3: Активируйте конфиг

```bash
ln -s /etc/nginx/sites-available/altersert /etc/nginx/sites-enabled/
```

### Шаг 8.4: Проверьте конфигурацию

```bash
nginx -t
```

Должно показать:
```
syntax is ok
test is successful
```

### Шаг 8.5: Перезапустите Nginx

```bash
systemctl restart nginx
```

### Шаг 8.6: Настройте права доступа

```bash
chown -R altersert:www-data /home/altersert/altersert_django
chmod -R 755 /home/altersert/altersert_django
```

---

## Часть 9: Настройка HTTPS (SSL сертификат)

### Шаг 9.1: Установите Certbot

```bash
apt install certbot python3-certbot-nginx -y
```

### Шаг 9.2: Получите сертификат

```bash
certbot --nginx -d your-domain.com -d www.your-domain.com
```

Введите:
- Email (для уведомлений)
- Согласитесь с условиями (A)
- Подпишитесь на рассылку или нет (Y/N)
- Выберите redirect (введите 2)

### Шаг 9.3: Проверьте автообновление

```bash
certbot renew --dry-run
```

---

## Часть 10: Финальная проверка

### Шаг 10.1: Проверьте статус сервисов

```bash
systemctl status nginx
supervisorctl status
```

### Шаг 10.2: Откройте сайт в браузере

Перейдите по адресу:
- `https://your-domain.com` (если настроили SSL)
- `http://your-domain.com` (если без SSL)
- `http://YOUR_SERVER_IP` (по IP)

### Шаг 10.3: Проверьте админ-панель

`https://your-domain.com/admin/`

Введите логин и пароль, созданные на шаге 6.5

---

## Часть 11: Управление сайтом

### Перезапуск сайта

```bash
supervisorctl restart altersert
```

### Просмотр логов

```bash
# Логи Gunicorn
tail -f /var/log/supervisor/altersert-stderr---supervisor-*.log

# Логи Nginx
tail -f /var/log/nginx/error.log
```

### Обновление кода (после изменений)

```bash
su - altersert
cd ~/altersert_django
git pull  # или загрузите новые файлы
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit
supervisorctl restart altersert
```

---

## Часть 12: Резервное копирование

### База данных

```bash
su - altersert
cd ~/altersert_django
source venv/bin/activate
python manage.py dumpdata > backup.json
```

### Восстановление из бэкапа

```bash
python manage.py loaddata backup.json
```

---

## Часть 13: Настройка firewall (рекомендуется)

```bash
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw enable
```

Проверьте статус:
```bash
ufw status
```

---

## Готово!

Ваш сайт работает по адресу:
- `https://your-domain.com` (с SSL)
- `http://your-domain.com` (без SSL)

Админ-панель:
- `https://your-domain.com/admin/`

---

## Часть 14: Устранение проблем

### Ошибка 502 Bad Gateway

**Проверьте Gunicorn:**
```bash
supervisorctl status
supervisorctl restart altersert
```

**Проверьте сокет:**
```bash
ls -la /home/altersert/altersert_django/app.sock
```

### Ошибка 403 Forbidden

**Проверьте права:**
```bash
chown -R altersert:www-data /home/altersert/altersert_django
chmod -R 755 /home/altersert/altersert_django
```

### Статические файлы не загружаются

```bash
su - altersert
cd ~/altersert_django
source venv/bin/activate
python manage.py collectstatic --noinput
exit
supervisorctl restart altersert
```

### Ошибка "Module not found"

```bash
su - altersert
cd ~/altersert_django
source venv/bin/activate
pip install -r requirements.txt
exit
supervisorctl restart altersert
```