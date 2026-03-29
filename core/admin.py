import logging

from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    SiteSettings, HeroSlide, Service, Project, ProjectImage,
    Advantage, WorkStep, PartnerProject, GalleryImage,
    PerspectiveInfo, PerspectiveStat, ContactRequest,
)

logger = logging.getLogger(__name__)

admin.site.site_header = 'ЕЛІТ-ФАСАД — Адміністрування'
admin.site.site_title = 'ЕЛІТ-ФАСАД CMS'
admin.site.index_title = 'Управління контентом'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основне', {'fields': ['company_name', 'slogan', 'logo', 'favicon']}),
        ('Контакти', {'fields': ['phone_main', 'phone_dev', 'address', 'email']}),
        ('Карта', {'fields': ['google_maps_embed_url']}),
        ('SEO', {'fields': ['meta_title', 'meta_description', 'og_image']}),
        ('Секція «Про компанію»', {'fields': [
            'about_title', 'about_subtitle', 'about_text_1', 'about_text_2',
        ]}),
        ('Заголовки секцій', {'fields': [
            'projects_title', 'projects_subtitle',
            'services_title',
            'experience_title', 'experience_subtitle',
            'gallery_title',
            'contacts_title', 'contacts_subtitle',
        ]}),
        ('Галерея — назви вкладок', {'fields': [
            'gallery_tab_realized', 'gallery_tab_completed', 'gallery_tab_perspective',
        ]}),
        ('Форма зворотного зв\'язку', {'fields': [
            'contact_form_text', 'contact_form_button',
            'contact_success_title', 'contact_success_text',
        ]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'preview']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception:
            logger.exception('HeroSlide save failed')
            raise

    def preview(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" style="max-height:60px;" />')
            except Exception:
                return '(broken url)'
        return ''
    preview.short_description = 'Зображення'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ['image_preview']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'status', 'year_completed', 'apartments_count', 'order']
    list_editable = ['order']
    list_filter = ['status', 'city']
    search_fields = ['name', 'address']
    inlines = [ProjectImageInline]


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'description', 'order']
    list_editable = ['order']


@admin.register(WorkStep)
class WorkStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title']


@admin.register(PartnerProject)
class PartnerProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_editable = ['order']
    list_filter = ['category']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'order', 'image_preview']
    list_editable = ['order']
    list_filter = ['category']
    readonly_fields = ['image_preview']


class PerspectiveStatInline(admin.TabularInline):
    model = PerspectiveStat
    extra = 1


@admin.register(PerspectiveInfo)
class PerspectiveInfoAdmin(admin.ModelAdmin):
    inlines = [PerspectiveStatInline]

    def has_add_permission(self, request):
        return not PerspectiveInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'object_type', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'phone']
    list_editable = ['is_read']
    readonly_fields = ['name', 'phone', 'object_type', 'message', 'created_at']

    def has_add_permission(self, request):
        return False
