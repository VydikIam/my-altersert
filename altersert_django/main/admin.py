from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from .models import (
    SiteSettings, Service, Advantage, WorkStep, 
    Application, PageVisit, DailyStats
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основные настройки', {
            'fields': ('site_name', 'logo', 'hero_image')
        }),
        ('Hero секция', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_button_primary', 'hero_button_secondary', 'hero_badge_1', 'hero_badge_2')
        }),
        ('Секция услуг', {
            'fields': ('services_title', 'services_subtitle')
        }),
        ('Секция преимуществ', {
            'fields': ('why_us_title', 'why_us_subtitle')
        }),
        ('Секция "Как мы работаем"', {
            'fields': ('how_it_works_title',)
        }),
        ('Секция контактов', {
            'fields': ('contact_title', 'contact_subtitle')
        }),
        ('Футер', {
            'fields': ('footer_text', 'address', 'phone', 'email')
        }),
        ('Социальные сети', {
            'fields': ('telegram', 'whatsapp')
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешаем добавить только если нет настроек
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'short_description', 'full_description')
        }),
        ('Медиа', {
            'fields': ('icon', 'image')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


@admin.register(WorkStep)
class WorkStepAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'description']
    list_editable = ['title', 'description']
    ordering = ['number']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'status', 'telegram_sent', 'created_at', 'view_details']
    list_filter = ['status', 'telegram_sent', 'created_at']
    search_fields = ['company_name', 'contact_person', 'phone', 'email', 'message']
    readonly_fields = ['ip_address', 'user_agent', 'referrer', 'created_at', 'updated_at', 'telegram_sent_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('company_name', 'contact_person', 'email', 'phone', 'message')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Telegram уведомление', {
            'fields': ('telegram_sent', 'telegram_sent_at')
        }),
        ('Техническая информация', {
            'fields': ('ip_address', 'user_agent', 'referrer', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_in_progress', 'mark_as_completed', 'mark_as_cancelled']
    
    def view_details(self, obj):
        return format_html('<a href="{}">Подробнее</a>', f'/admin/main/application/{obj.id}/change/')
    view_details.short_description = 'Действия'
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = 'Отметить как "В обработке"'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = 'Отметить как "Завершена"'
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Отметить как "Отменена"'


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['page', 'ip_address', 'session_key', 'created_at']
    list_filter = ['created_at', 'page']
    search_fields = ['page', 'ip_address', 'user_agent']
    readonly_fields = ['page', 'ip_address', 'user_agent', 'referrer', 'session_key', 'country', 'city', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'visits', 'unique_visitors', 'applications', 'conversion_rate']
    readonly_fields = ['date', 'visits', 'unique_visitors', 'applications']
    date_hierarchy = 'date'
    
    def conversion_rate(self, obj):
        if obj.visits == 0:
            return '0%'
        rate = (obj.applications / obj.visits) * 100
        return f'{rate:.2f}%'
    conversion_rate.short_description = 'Конверсия'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Кастомная админка
admin.site.site_header = 'Альтер Серт - Администрирование'
admin.site.site_title = 'Альтер Серт'
admin.site.index_title = 'Управление сайтом'