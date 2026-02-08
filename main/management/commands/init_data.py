#!/usr/bin/env python
"""
Команда для инициализации начальных данных
"""
from django.core.management.base import BaseCommand
from main.models import SiteSettings, Service, Advantage, WorkStep


class Command(BaseCommand):
    help = 'Инициализация начальных данных сайта'

    def handle(self, *args, **options):
        self.stdout.write('Инициализация данных...')
        
        # Создаём настройки сайта
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Альтер Серт',
                'hero_title': 'Профессиональная Сертификация и Легализация',
                'hero_subtitle': 'Ваш надёжный партнёр в мире сертификации. Полное соответствие законодательству и регламентам.',
                'hero_button_primary': 'Рассчитать стоимость',
                'hero_button_secondary': 'Получить консультацию',
                'hero_badge_1': '100% Легально',
                'hero_badge_2': 'Быстрее на 40%',
                'services_title': 'Наши Услуги',
                'services_subtitle': 'Полный спектр услуг по легализации продукции. От разработки документов до получения сертификатов.',
                'why_us_title': 'Почему Альтер Серт?',
                'why_us_subtitle': 'Мы объединили многолетний опыт экспертов и передовые технологии для вашего спокойствия.',
                'how_it_works_title': 'Как мы работаем',
                'contact_title': 'Оставить заявку',
                'contact_subtitle': 'Заполните форму, и мы свяжемся с вами в течение 15 минут для расчёта стоимости.',
                'footer_text': 'Ваш надёжный партнёр в мире сертификации. Полное соответствие регламентам.',
                'address': 'г. Москва, ул. Примерная, д. 10, оф. 305',
                'phone': '+7 (495) 000-00-00',
                'email': 'info@altersert.ru',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Настройки сайта созданы'))
        else:
            self.stdout.write('✓ Настройки сайта уже существуют')
        
        # Создаём услуги
        services_data = [
            {
                'title': 'Сертификация',
                'slug': 'certification',
                'short_description': 'Оформление сертификатов соответствия ТР ТС и ГОСТ Р.',
                'full_description': 'Полное сопровождение процесса получения сертификатов соответствия техническим регламентам Таможенного союза и ГОСТ Р. Мы помогаем собрать необходимый пакет документов, проводим испытания и получаем сертификат в кратчайшие сроки.',
                'order': 1,
            },
            {
                'title': 'Декларирование',
                'slug': 'declaration',
                'short_description': 'Регистрация деклараций о соответствии продукции.',
                'full_description': 'Оформление деклараций о соответствии для продукции, подпадающей под действие технических регламентов. Помогаем с подготовкой документов и регистрацией декларации в едином реестре.',
                'order': 2,
            },
            {
                'title': 'Разработка ТУ',
                'slug': 'tu',
                'short_description': 'Разработка и регистрация технических условий.',
                'full_description': 'Профессиональная разработка технических условий (ТУ) для вашей продукции. Регистрация ТУ в установленном порядке. Гарантируем соответствие всем нормативным требованиям.',
                'order': 3,
            },
            {
                'title': 'Этикетки',
                'slug': 'labels',
                'short_description': 'Проверка и разработка макетов этикеток по регламентам.',
                'full_description': 'Разработка и проверка макетов этикеток на соответствие требованиям технических регламентов. Консультации по маркировке продукции.',
                'order': 4,
            },
            {
                'title': 'Товарный знак',
                'slug': 'trademark',
                'short_description': 'Регистрация и защита интеллектуальной собственности.',
                'full_description': 'Полное сопровождение регистрации товарного знака. Проверка на тождество и сходство, подготовка документов, ведение делопроизводства.',
                'order': 5,
            },
            {
                'title': 'Честный ЗНАК',
                'slug': 'markirovka',
                'short_description': 'Подключение к системе маркировки и сопровождение.',
                'full_description': 'Помощь в подключении к системе маркировки "Честный ЗНАК". Обучение работе с системой, сопровождение при маркировке товаров.',
                'order': 6,
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Услуга "{service.title}" создана'))
        
        # Создаём преимущества
        advantages_data = [
            {
                'title': 'Автоматизация',
                'description': 'Используем современные технологии для анализа документов, что исключает ошибки и ускоряет процесс.',
                'order': 1,
            },
            {
                'title': 'Скорость',
                'description': 'Получение сертификатов и деклараций до 40% быстрее благодаря цифровизации процессов.',
                'order': 2,
            },
            {
                'title': 'Экспертиза',
                'description': 'Команда аккредитованных экспертов с опытом работы более 10 лет.',
                'order': 3,
            },
            {
                'title': 'Экономия',
                'description': 'Оптимизация процессов позволяет нам предлагать лучшие цены на рынке.',
                'order': 4,
            },
        ]
        
        for advantage_data in advantages_data:
            advantage, created = Advantage.objects.get_or_create(
                title=advantage_data['title'],
                defaults=advantage_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Преимущество "{advantage.title}" создано'))
        
        # Создаём этапы работы
        steps_data = [
            {
                'number': 1,
                'title': 'Заявка',
                'description': 'Вы оставляете заявку на сайте или по телефону.',
            },
            {
                'number': 2,
                'title': 'Анализ',
                'description': 'Наши эксперты анализируют вашу продукцию и требования.',
            },
            {
                'number': 3,
                'title': 'Документы',
                'description': 'Мы готовим полный пакет документов для сертификации.',
            },
            {
                'number': 4,
                'title': 'Результат',
                'description': 'Вы получаете готовый сертификат или декларацию.',
            },
        ]
        
        for step_data in steps_data:
            step, created = WorkStep.objects.get_or_create(
                number=step_data['number'],
                defaults=step_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Этап "{step.title}" создан'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Инициализация завершена успешно!'))