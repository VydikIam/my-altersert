from django.utils import timezone
from .models import PageVisit, DailyStats


class VisitTrackingMiddleware:
    """Middleware для отслеживания посещений страниц"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Пропускаем статические файлы и медиа
        if request.path.startswith(('/static/', '/media/', '/admin/')):
            return self.get_response(request)
        
        # Пропускаем AJAX запросы
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.get_response(request)
        
        response = self.get_response(request)
        
        # Записываем посещение только для успешных ответов
        if response.status_code == 200:
            self.track_visit(request)
        
        return response
    
    def track_visit(self, request):
        """Запись посещения"""
        try:
            # Получаем IP адрес
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Получаем или создаём сессию
            if not request.session.session_key:
                request.session.create()
            
            session_key = request.session.session_key
            
            # Создаём запись о посещении
            PageVisit.objects.create(
                page=request.path,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referrer=request.META.get('HTTP_REFERER', '')[:500] if request.META.get('HTTP_REFERER') else None,
                session_key=session_key
            )
            
            # Обновляем ежедневную статистику
            today = timezone.now().date()
            stats, created = DailyStats.objects.get_or_create(date=today)
            stats.visits += 1
            
            # Подсчитываем уникальных посетителей за сегодня
            unique_today = PageVisit.objects.filter(
                created_at__date=today
            ).values('session_key').distinct().count()
            stats.unique_visitors = unique_today
            
            stats.save()
            
        except Exception as e:
            # Логируем ошибку, но не прерываем запрос
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Error tracking visit: {str(e)}')