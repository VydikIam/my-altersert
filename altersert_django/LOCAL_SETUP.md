# Запуск на локальном компьютере (Windows / Mac / Linux)

## Часть 1: Подготовка

### Шаг 1.1: Установите Python

**Windows:**
1. Откройте браузер
2. Перейдите на https://www.python.org/downloads/
3. Скачайте Python 3.11 или выше
4. Запустите установщик
5. **ВАЖНО:** Поставьте галочку "Add Python to PATH"
6. Нажмите "Install Now"
7. Дождитесь окончания установки

**Mac:**
1. Откройте Терминал (Terminal)
2. Проверьте версию Python:
```bash
python3 --version
```
3. Если Python не установлен или версия ниже 3.11:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Шаг 1.2: Проверьте установку Python

Откройте терминал/командную строку и введите:

```bash
python --version
```

или на Mac/Linux:

```bash
python3 --version
```

Должно показать версию 3.11 или выше.

---

## Часть 2: Скачивание проекта

### Шаг 2.1: Создайте папку для проекта

**Windows (в командной строке cmd):**
```cmd
mkdir C:\projects
cd C:\projects
```

**Mac/Linux:**
```bash
mkdir ~/projects
cd ~/projects
```

### Шаг 2.2: Скачайте проект

Если у вас ZIP-архив:

**Windows:**
1. Распакуйте архив `altersert_django.zip` в папку `C:\projects\`
2. Должна появиться папка `C:\projects\altersert_django`

**Mac/Linux:**
```bash
unzip altersert_django.zip
```

Или если через git:
```bash
git clone <ссылка-на-репозиторий>
```

### Шаг 2.3: Перейдите в папку проекта

**Windows:**
```cmd
cd C:\projects\altersert_django
```

**Mac/Linux:**
```bash
cd ~/projects/altersert_django
```

---

## Часть 3: Создание виртуального окружения

### Шаг 3.1: Создайте виртуальное окружение

**Windows:**
```cmd
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

Вы увидите созданную папку `venv` внутри проекта.

### Шаг 3.2: Активируйте виртуальное окружение

**Windows (cmd):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Если PowerShell выдаёт ошибку политики, выполните:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Шаг 3.3: Проверьте активацию

После активации в начале строки должно появиться `(venv)`:

```
(venv) C:\projects\altersert_django>
```

или

```
(venv) ~/projects/altersert_django$
```

---

## Часть 4: Установка зависимостей

### Шаг 4.1: Обновите pip

```bash
pip install --upgrade pip
```

### Шаг 4.2: Установите все зависимости

```bash
pip install -r requirements.txt
```

Это установит:
- Django 4.2+
- Pillow (для работы с изображениями)
- requests (для Telegram)
- python-dotenv (для .env файлов)
- whitenoise (для статических файлов)

Ждите окончания установки. Должно появиться сообщение "Successfully installed ..."

---

## Часть 5: Создание файла .env

### Шаг 5.1: Создайте файл .env

**Windows (в cmd):**
```cmd
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### Шаг 5.2: Откройте файл .env для редактирования

**Windows:**
```cmd
notepad .env
```

**Mac:**
```bash
open -e .env
```

**Linux:**
```bash
nano .env
```

### Шаг 5.3: Отредактируйте файл .env

Удалите всё содержимое и вставьте это (замените значения на свои):

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-this-to-random-string-50-chars-long
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Telegram Bot Settings (опционально)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@example.com
```

**ВАЖНО:** SECRET_KEY должен быть длинной строкой (50+ символов). Сгенерируйте его:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Скопируйте полученную строку и вставьте вместо `your-secret-key-here...`

### Шаг 5.4: Сохраните файл

**Windows (Notepad):** Ctrl+S, затем закройте
**Mac (TextEdit):** Cmd+S, затем закройте
**Linux (nano):** Ctrl+O, Enter, Ctrl+X

---

## Часть 6: Настройка базы данных

### Шаг 6.1: Примените миграции

Убедитесь, что виртуальное окружение активно (видите `(venv)` в начале строки), затем:

```bash
python manage.py migrate
```

Вы увидите много строк с "Applying main.0001_initial... OK"

### Шаг 6.2: Создайте суперпользователя

```bash
python manage.py createsuperuser
```

Вас попросят ввести:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`
- Password (again): `admin123`

Если спросит "Bypass password validation?" - введите `y`

### Шаг 6.3: Загрузите начальные данные

```bash
python manage.py init_data
```

Вы увидите:
```
Инициализация данных...
✓ Настройки сайта созданы
✓ Услуга "Сертификация" создана
✓ Услуга "Декларирование" создана
...
✅ Инициализация завершена успешно!
```

### Шаг 6.4: Соберите статические файлы

```bash
python manage.py collectstatic --noinput
```

---

## Часть 7: Запуск сервера

### Шаг 7.1: Запустите сервер разработки

```bash
python manage.py runserver
```

Вы увидите:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues.

January 15, 2026 - 10:30:00
Django version 4.2.0, using settings 'altersert.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Шаг 7.2: Откройте сайт в браузере

Перейдите по адресу: **http://127.0.0.1:8000/**

### Шаг 7.3: Проверьте админ-панель

Перейдите по адресу: **http://127.0.0.1:8000/admin/**

Введите:
- Логин: `admin`
- Пароль: `admin123`

---

## Часть 8: Остановка сервера

### Шаг 8.1: Остановите сервер

В терминале, где запущен сервер, нажмите:

**Windows:** `Ctrl + C` (дважды)
**Mac/Linux:** `Ctrl + C`

### Шаг 8.2: Деактивируйте виртуальное окружение

```bash
deactivate
```

---

## Часть 9: Повторный запуск (после перезагрузки компьютера)

### Шаг 9.1: Откройте терминал и перейдите в папку проекта

**Windows:**
```cmd
cd C:\projects\altersert_django
```

**Mac/Linux:**
```bash
cd ~/projects/altersert_django
```

### Шаг 9.2: Активируйте виртуальное окружение

**Windows:**
```cmd
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Шаг 9.3: Запустите сервер

```bash
python manage.py runserver
```

---

## Часть 10: Настройка Telegram уведомлений (опционально)

### Шаг 10.1: Создайте бота

1. Откройте Telegram
2. Найдите бота **@BotFather**
3. Отправьте команду `/newbot`
4. Введите имя бота (например: "Альтер Серт Уведомления")
5. Введите username бота (например: "altersert_bot")
6. Получите токен вида: `123456789:ABCdefGHIjklMNOpqrSTUvwxyz`

### Шаг 10.2: Узнайте свой chat_id

1. Найдите бота **@userinfobot**
2. Отправьте ему любое сообщение
3. Он ответит вашим ID (например: `123456789`)

### Шаг 10.3: Отправьте сообщение своему боту

1. Найдите своего бота по username (например: @altersert_bot)
2. Отправьте ему `/start`

### Шаг 10.4: Отредактируйте .env

Откройте файл `.env` и добавьте:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
TELEGRAM_CHAT_ID=123456789
```

Замените значения на свои!

### Шаг 10.5: Перезапустите сервер

Остановите сервер (Ctrl+C) и запустите снова:

```bash
python manage.py runserver
```

Теперь при отправке заявки на сайте, вам будет приходить уведомление в Telegram!

---

## Часть 11: Устранение ошибок

### Ошибка: "'python' is not recognized"

**Решение для Windows:**
1. Переустановите Python с галочкой "Add Python to PATH"
2. Или используйте `py` вместо `python`

### Ошибка: "No module named 'django'"

**Решение:**
```bash
pip install django
```

Или повторите:
```bash
pip install -r requirements.txt
```

### Ошибка: "Port 8000 is already in use"

**Решение:**
```bash
python manage.py runserver 8001
```

Или найдите и закройте процесс, занимающий порт 8000.

### Ошибка: "Access denied" при активации venv в PowerShell

**Решение:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Готово!

Ваш сайт работает по адресу: **http://127.0.0.1:8000/**

Админ-панель: **http://127.0.0.1:8000/admin/**