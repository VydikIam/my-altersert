from .models import SiteSettings


def site_settings(request):
    """Контекстный процессор для настроек сайта"""
    try:
        settings_obj = SiteSettings.objects.first()
        if not settings_obj:
            settings_obj = SiteSettings.objects.create()
    except:
        settings_obj = None
    
    return {
        'site_settings': settings_obj,
    }