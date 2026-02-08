#!/usr/bin/env python
"""
Скрипт для быстрой настройки проекта
"""
import os
import sys
import secrets


def generate_secret_key():
    """Генерация случайного SECRET_KEY"""
    return secrets.token_urlsafe(50)


def main():
    print("=" * 60)
    print("Настройка проекта Альтер Серт")
    print("=" * 60)
    
    # Проверяем наличие .env
    env_file = '.env'
    env_example = '.env.example'
    
    if not os.path.exists(env_file):
        print("\n1. Создание файла .env...")
        
        # Читаем пример
        with open(env_example, 'r') as f:
            content = f.read()
        
        # Генерируем новый SECRET_KEY
        secret_key = generate_secret_key()
        content = content.replace('your-secret-key-here-change-in-production', secret_key)
        
        # Записываем .env
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"   ✓ Файл .env создан с SECRET_KEY")
    else:
        print("\n1. Файл .env уже существует")
    
    # Применяем миграции
    print("\n2. Применение миграций...")
    os.system('python manage.py migrate')
    
    # Создаём суперпользователя
    print("\n3. Создание суперпользователя...")
    print("   (Если пользователь уже существует, будет ошибка - это нормально)")
    os.system('python manage.py createsuperuser --username=admin --email=admin@example.com --noinput || true')
    
    # Устанавливаем пароль для суперпользователя
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(username='admin')
        user.set_password('admin123')
        user.save()
        print("   ✓ Суперпользователь admin создан")
        print("   Логин: admin")
        print("   Пароль: admin123")
    except:
        pass
    
    # Загружаем начальные данные
    print("\n4. Загрузка начальных данных...")
    os.system('python manage.py init_data')
    
    # Собираем статические файлы
    print("\n5. Сбор статических файлов...")
    os.system('python manage.py collectstatic --noinput')
    
    print("\n" + "=" * 60)
    print("Настройка завершена!")
    print("=" * 60)
    print("\nЗапуск сервера:")
    print("  python manage.py runserver")
    print("\nАдмин-панель:")
    print("  http://127.0.0.1:8000/admin/")
    print("  Логин: admin")
    print("  Пароль: admin123")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    # Настраиваем Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'altersert.settings')
    
    import django
    django.setup()
    
    main()