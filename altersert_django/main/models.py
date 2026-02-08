from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    """Настройки сайта"""
    site_name = models.CharField('Название сайта', max_length=100, default='Альтер Серт')
    logo = models.ImageField('Логотип', upload_to='site/', blank=True, null=True)
    
    # Hero section
    hero_title = models.CharField('Заголовок Hero', max_length=200, default='Профессиональная Сертификация и Легализация')
    hero_subtitle = models.TextField('Подзаголовок Hero', default='Ваш надёжный партнёр в мире сертификации. Полное соответствие законодательству и регламентам.')
    hero_image = models.ImageField('Изображение Hero', upload_to='site/', blank=True, null=True)
    hero_button_primary = models.CharField('Текст основной кнопки', max_length=50, default='Рассчитать стоимость')
    hero_button_secondary = models.CharField('Текст вторичной кнопки', max_length=50, default='Получить консультацию')
    hero_badge_1 = models.CharField('Бейдж 1', max_length=50, default='100% Легально')
    hero_badge_2 = models.CharField('Бейдж 2', max_length=50, default='Быстрее на 40%')
    
    # Services section
    services_title = models.CharField('Заголовок услуг', max_length=100, default='Наши Услуги')
    services_subtitle = models.TextField('Подзаголовок услуг', default='Полный спектр услуг по легализации продукции. От разработки документов до получения сертификатов.')
    
    # Why us section
    why_us_title = models.CharField('Заголовок "Почему мы"', max_length=100, default='Почему Альтер Серт?')
    why_us_subtitle = models.TextField('Подзаголовок "Почему мы"', default='Мы объединили многолетний опыт экспертов и передовые технологии для вашего спокойствия.')
    
    # How it works section
    how_it_works_title = models.CharField('Заголовок "Как мы работаем"', max_length=100, default='Как мы работаем')
    
    # Contact section
    contact_title = models.CharField('Заголовок контактов', max_length=100, default='Оставить заявку')
    contact_subtitle = models.TextField('Подзаголовок контактов', default='Заполните форму, и мы свяжемся с вами в течение 15 минут для расчёта стоимости.')
    
    # Footer
    footer_text = models.TextField('Текст в футере', default='Ваш надёжный партнёр в мире сертификации. Полное соответствие регламентам.')
    address = models.CharField('Адрес', max_length=200, default='г. Москва, ул. Примерная, д. 10, оф. 305')
    phone = models.CharField('Телефон', max_length=50, default='+7 (495) 000-00-00')
    email = models.EmailField('Email', default='info@altersert.ru')
    
    # Social links
    telegram = models.URLField('Telegram', blank=True, null=True)
    whatsapp = models.URLField('WhatsApp', blank=True, null=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
    
    def __str__(self):
        return 'Настройки сайта'
    
    def save(self, *args, **kwargs):
        if SiteSettings.objects.exists() and not self.pk:
            # Если уже есть настройки, удаляем их перед сохранением новых
            SiteSettings.objects.all().delete()
        super().save(*args, **kwargs)


class Service(models.Model):
    """Услуги"""
    title = models.CharField('Название услуги', max_length=100)
    slug = models.SlugField('URL', unique=True)
    short_description = models.TextField('Краткое описание', max_length=200)
    full_description = models.TextField('Полное описание', blank=True)
    icon = models.CharField('Иконка (SVG или класс)', max_length=500, blank=True, help_text='SVG код или CSS класс иконки')
    image = models.ImageField('Изображение', upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class Advantage(models.Model):
    """Преимущества"""
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', max_length=300)
    icon = models.CharField('Иконка (SVG или класс)', max_length=500, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class WorkStep(models.Model):
    """Этапы работы"""
    number = models.PositiveIntegerField('Номер этапа', unique=True)
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', max_length=300)
    
    class Meta:
        verbose_name = 'Этап работы'
        verbose_name_plural = 'Этапы работы'
        ordering = ['number']
    
    def __str__(self):
        return f'{self.number}. {self.title}'


class Application(models.Model):
    """Заявки от клиентов"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    company_name = models.CharField('Название компании / Имя', max_length=200)
    contact_person = models.CharField('Контактное лицо', max_length=200, blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=50)
    message = models.TextField('Сообщение / Услуга', blank=True)
    
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Telegram notification
    telegram_sent = models.BooleanField('Уведомление отправлено', default=False)
    telegram_sent_at = models.DateTimeField('Время отправки уведомления', blank=True, null=True)
    
    # Tracking
    ip_address = models.GenericIPAddressField('IP адрес', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    referrer = models.URLField('Источник', blank=True, null=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.company_name} - {self.phone}'


class PageVisit(models.Model):
    """Посещения страниц"""
    page = models.CharField('Страница', max_length=200)
    ip_address = models.GenericIPAddressField('IP адрес', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    referrer = models.URLField('Источник', blank=True, null=True)
    session_key = models.CharField('Ключ сессии', max_length=40, blank=True)
    
    # Geo info (if available)
    country = models.CharField('Страна', max_length=100, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    
    created_at = models.DateTimeField('Время посещения', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.page} - {self.ip_address}'


class DailyStats(models.Model):
    """Ежедневная статистика"""
    date = models.DateField('Дата', unique=True)
    visits = models.PositiveIntegerField('Посещения', default=0)
    unique_visitors = models.PositiveIntegerField('Уникальные посетители', default=0)
    applications = models.PositiveIntegerField('Заявки', default=0)
    
    class Meta:
        verbose_name = 'Ежедневная статистика'
        verbose_name_plural = 'Ежедневная статистика'
        ordering = ['-date']
    
    def __str__(self):
        return f'{self.date}: {self.visits} посещений, {self.applications} заявок'