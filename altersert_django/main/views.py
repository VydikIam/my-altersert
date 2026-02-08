import requests
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from .models import (
    SiteSettings, Service, Advantage, WorkStep, 
    Application, PageVisit, DailyStats
)

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_telegram_notification(application):
    """Отправка уведомления в Telegram о новой заявке"""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning('Telegram settings not configured')
        return False
    
    message = f"""🆕 <b>Новая заявка!</b>

🏢 <b>Компания/Имя:</b> {application.company_name}
👤 <b>Контактное лицо:</b> {application.contact_person or 'Не указано'}
📧 <b>Email:</b> {application.email or 'Не указан'}
📱 <b>Телефон:</b> {application.phone}
💬 <b>Сообщение:</b> {application.message or 'Не указано'}

🌐 <b>IP:</b> {application.ip_address or 'Неизвестен'}
⏰ <b>Время:</b> {application.created_at.strftime('%d.%m.%Y %H:%M:%S')}
"""
    
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            application.telegram_sent = True
            application.telegram_sent_at = timezone.now()
            application.save(update_fields=['telegram_sent', 'telegram_sent_at'])
            logger.info(f'Telegram notification sent for application {application.id}')
            return True
        else:
            logger.error(f'Telegram API error: {response.text}')
            return False
            
    except Exception as e:
        logger.error(f'Error sending Telegram notification: {str(e)}')
        return False


def index(request):
    """Главная страница"""
    # Получаем или создаём настройки
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    
    services = Service.objects.filter(is_active=True)
    advantages = Advantage.objects.filter(is_active=True)
    work_steps = WorkStep.objects.all()
    
    context = {
        'site_settings': site_settings,
        'services': services,
        'advantages': advantages,
        'work_steps': work_steps,
    }
    
    return render(request, 'main/index.html', context)


def about(request):
    """Страница О нас"""
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'main/about.html', context)


def blog(request):
    """Страница Блог"""
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'main/blog.html', context)


def contacts(request):
    """Страница Контакты"""
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'main/contacts.html', context)


def service_detail(request, slug):
    """Детальная страница услуги"""
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    service = Service.objects.get(slug=slug, is_active=True)
    
    context = {
        'site_settings': site_settings,
        'service': service,
    }
    return render(request, 'main/service_detail.html', context)


@require_http_methods(["POST"])
def submit_application(request):
    """Обработка отправки заявки"""
    try:
        company_name = request.POST.get('company_name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Валидация
        if not company_name or not phone:
            return JsonResponse({
                'success': False,
                'message': 'Пожалуйста, заполните обязательные поля (Имя/Компания и Телефон)'
            })
        
        # Создаём заявку
        application = Application.objects.create(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            message=message,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            referrer=request.META.get('HTTP_REFERER', '')
        )
        
        # Обновляем статистику
        today = timezone.now().date()
        stats, _ = DailyStats.objects.get_or_create(date=today)
        stats.applications += 1
        stats.save()
        
        # Отправляем уведомление в Telegram
        send_telegram_notification(application)
        
        return JsonResponse({
            'success': True,
            'message': 'Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.'
        })
        
    except Exception as e:
        logger.error(f'Error submitting application: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже.'
        })


def get_stats(request):
    """API для получения статистики (для админки)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    today = timezone.now().date()
    
    # Статистика за сегодня
    today_stats, _ = DailyStats.objects.get_or_create(date=today)
    
    # Заявки за последние 7 дней
    last_7_days = DailyStats.objects.filter(
        date__gte=today - timezone.timedelta(days=7)
    ).order_by('date')
    
    # Общая статистика
    total_visits = PageVisit.objects.count()
    total_applications = Application.objects.count()
    total_unique_visitors = PageVisit.objects.values('session_key').distinct().count()
    
    # Заявки по статусам
    applications_by_status = Application.objects.values('status').annotate(
        count=Count('id')
    )
    
    return JsonResponse({
        'today': {
            'visits': today_stats.visits,
            'applications': today_stats.applications,
            'unique_visitors': today_stats.unique_visitors,
        },
        'total': {
            'visits': total_visits,
            'applications': total_applications,
            'unique_visitors': total_unique_visitors,
        },
        'last_7_days': list(last_7_days.values('date', 'visits', 'applications')),
        'applications_by_status': list(applications_by_status),
    })