# Быстрый старт (для опытных пользователей)

## Локальный запуск

```bash
# 1. Перейдите в папку проекта
cd altersert_django

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте окружение
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Установите зависимости
pip install -r requirements.txt

# 5. Создайте .env файл
cp .env.example .env
# Отредактируйте .env (установите SECRET_KEY)

# 6. Примените миграции
python manage.py migrate

# 7. Создайте суперпользователя
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# 8. Загрузите начальные данные
python manage.py init_data

# 9. Соберите статику
python manage.py collectstatic --noinput

# 10. Запустите сервер
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/
Админка: http://127.0.0.1:8000/admin/

---

## Повторный запуск (после перезагрузки)

```bash
cd altersert_django
source venv/bin/activate  # или venv\Scripts\activate на Windows
python manage.py runserver
```

---

## Развёртывание на сервере (Ubuntu)

```bash
# 1. Подключитесь к серверу
ssh root@YOUR_SERVER_IP

# 2. Обновите систему
apt update && apt upgrade -y

# 3. Установите зависимости
apt install python3 python3-pip python3-venv nginx supervisor git -y

# 4. Создайте пользователя
useradd -m -s /bin/bash altersert
passwd altersert
usermod -aG sudo altersert

# 5. Переключитесь на пользователя
su - altersert

# 6. Загрузите проект
git clone https://github.com/yourusername/altersert_django.git
cd altersert_django

# 7. Настройте окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 8. Настройте .env
nano .env
# DEBUG=False
# SECRET_KEY=your-secret-key
# ALLOWED_HOSTS=your-domain.com

# 9. Примените миграции и соберите статику
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
python manage.py collectstatic --noinput

# 10. Выйдите из пользователя
exit

# 11. Настройте Supervisor
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
```

```bash
supervisorctl reread
supervisorctl update
supervisorctl start altersert

# 12. Настройте Nginx
nano /etc/nginx/sites-available/altersert
```

Вставьте:
```nginx
server {
    listen 80;
    server_name your-domain.com;

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

```bash
ln -s /etc/nginx/sites-available/altersert /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# 13. Настройте SSL (опционально)
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

Готово! Сайт доступен по https://your-domain.com