import logging

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

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
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = [
        ('Основне', {'fields': [('company_name', 'slogan'), ('logo', 'favicon')]}),
        ('Контакти', {'fields': [('phone_main', 'phone_dev'), 'address', 'email']}),
        ('Карта', {'fields': ['google_maps_embed_url']}),
        ('SEO', {'fields': ['meta_title', 'meta_description', 'og_image']}),
        ('Секція «Про компанію»', {'fields': [
            'about_title', 'about_subtitle', 'about_text_1', 'about_text_2',
        ]}),
        ('Заголовки секцій', {'fields': [
            ('projects_title', 'projects_subtitle'),
            'services_title',
            ('experience_title', 'experience_subtitle'),
            'gallery_title',
            ('contacts_title', 'contacts_subtitle'),
        ]}),
        ('Галерея — назви вкладок', {'fields': [
            'gallery_tab_realized', 'gallery_tab_completed', 'gallery_tab_perspective',
        ]}),
        ("Форма зворотного зв'язку", {'fields': [
            'contact_form_text', 'contact_form_button',
            ('contact_success_title', 'contact_success_text'),
        ]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1, defaults={
            'phone_main': '+38 (050) 304 74 62',
        })
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk])
        )


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ['title', 'order', 'get_is_active', 'get_image_preview']
    list_editable = ['order']
    list_filter = ['is_active']
    list_per_page = 20

    @display(description='Активний', boolean=True)
    def get_is_active(self, obj):
        return obj.is_active

    @display(description='Зображення')
    def get_image_preview(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" style="max-height:60px;border-radius:4px;" />', obj.image.url)
            except Exception:
                return '(помилка)'
        return '—'

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception:
            logger.exception('HeroSlide save failed')
            raise


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'order', 'get_is_active']
    list_editable = ['order']
    list_per_page = 25

    @display(description='Активна', boolean=True)
    def get_is_active(self, obj):
        return obj.is_active


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ['get_image_preview']
    fields = ['image', 'get_image_preview', 'caption', 'is_cover', 'order']

    @display(description='Превʼю')
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;border-radius:4px;" />', obj.image.url)
        return '—'


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['name', 'city', 'get_status_badge', 'year_completed', 'apartments_count', 'order']
    list_editable = ['order']
    list_filter = ['status', 'city']
    search_fields = ['name', 'address']
    inlines = [ProjectImageInline]
    list_per_page = 20

    @display(description='Статус', label={
        'completed': 'success',
        'in_progress': 'warning',
        'planned': 'info',
    })
    def get_status_badge(self, obj):
        return obj.status


@admin.register(Advantage)
class AdvantageAdmin(ModelAdmin):
    list_display = ['title', 'value', 'description', 'order']
    list_editable = ['order']
    list_per_page = 25


@admin.register(WorkStep)
class WorkStepAdmin(ModelAdmin):
    list_display = ['step_number', 'title']
    list_per_page = 25


@admin.register(PartnerProject)
class PartnerProjectAdmin(ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_editable = ['order']
    list_filter = ['category']
    list_per_page = 25


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ['get_caption', 'category', 'order', 'get_image_preview']
    list_editable = ['order']
    list_filter = ['category']
    readonly_fields = ['get_image_preview']
    list_per_page = 20

    @display(description='Підпис')
    def get_caption(self, obj):
        return obj.caption or f'Зображення #{obj.pk}'

    @display(description='Превʼю')
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;border-radius:4px;" />', obj.image.url)
        return '—'


class PerspectiveStatInline(TabularInline):
    model = PerspectiveStat
    extra = 1
    fields = ['label', 'value', 'suffix', 'order']


@admin.register(PerspectiveInfo)
class PerspectiveInfoAdmin(ModelAdmin):
    inlines = [PerspectiveStatInline]
    fieldsets = [
        ('Основне', {'fields': ['title', 'subtitle', 'description', 'location', 'hero_image']}),
    ]

    def has_add_permission(self, request):
        return not PerspectiveInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = PerspectiveInfo.objects.get_or_create(pk=1, defaults={'description': ''})
        return HttpResponseRedirect(
            reverse('admin:core_perspectiveinfo_change', args=[obj.pk])
        )


@admin.register(ContactRequest)
class ContactRequestAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'object_type', 'created_at', 'get_is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['name', 'phone', 'object_type', 'message', 'created_at']
    list_per_page = 25

    @display(description='Прочитано', label={True: 'success', False: 'danger'})
    def get_is_read(self, obj):
        return obj.is_read

    def has_add_permission(self, request):
        return False
