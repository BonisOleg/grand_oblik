from django.db import models
from django.utils.html import mark_safe


class SiteSettings(models.Model):
    company_name = models.CharField('Назва компанії', max_length=200, default='Гранд Облік')
    slogan = models.CharField('Слоган', max_length=300, blank=True)
    phone_main = models.CharField('Основний телефон', max_length=30)
    phone_dev = models.CharField('Телефон відділу розвитку', max_length=30, blank=True)
    address = models.TextField('Адреса')
    email = models.EmailField('Email', blank=True)
    logo = models.ImageField('Логотип', upload_to='site/', blank=True)
    favicon = models.ImageField('Favicon', upload_to='site/', blank=True)
    google_maps_embed_url = models.TextField('Google Maps embed (iframe)', blank=True)
    meta_title = models.CharField('Meta Title', max_length=200, blank=True)
    meta_description = models.TextField('Meta Description', blank=True)
    og_image = models.ImageField('OG Image', upload_to='site/', blank=True)

    # Секція "Про компанію"
    about_title = models.CharField('Заголовок блоку "Про нас"', max_length=200, default='Аграрний сектор')
    about_subtitle = models.CharField('Підзаголовок блоку "Про нас"', max_length=300, blank=True)
    about_text_1 = models.TextField('Перший абзац "Про нас"', blank=True)
    about_text_2 = models.TextField('Другий абзац "Про нас"', blank=True)

    # Заголовки секцій
    projects_title = models.CharField('Секція "Об\'єкти" — заголовок', max_length=200, default='Реєстрація бізнесу')
    projects_subtitle = models.CharField('Секція "Об\'єкти" — підзаголовок', max_length=300, default='Відкриття, закриття та внесення змін')
    services_title = models.CharField('Секція "Послуги" — заголовок', max_length=200, default='Наші послуги')
    experience_title = models.CharField('Секція "Досвід" — заголовок', max_length=200, default='Послуги для ФОП')
    experience_subtitle = models.CharField('Секція "Досвід" — підзаголовок', max_length=300, default='Повний супровід ФОП на будь-якій системі оподаткування')
    gallery_title = models.CharField('Секція "Галерея" — заголовок', max_length=200, default='Галерея')
    gallery_tab_realized = models.CharField('Галерея — вкладка "Реалізовані"', max_length=100, default='Реалізовані об\'єкти')
    gallery_tab_completed = models.CharField('Галерея — вкладка "Вишгород"', max_length=100, default='Об\'єкти Вишгород')
    gallery_tab_perspective = models.CharField('Галерея — вкладка "Перспективні"', max_length=100, default='Перспективні проєкти')
    contacts_title = models.CharField('Секція "Контакти" — заголовок', max_length=200, default='Контакти')
    contacts_subtitle = models.CharField('Секція "Контакти" — підзаголовок', max_length=300, default="Залишилися питання? Зв'яжіться з нами")

    # Форма зворотного зв'язку
    contact_form_text = models.CharField(
        'Текст над формою', max_length=300,
        default='Заповніть форму і наш менеджер зателефонує вам найближчим часом',
    )
    contact_form_button = models.CharField('Текст кнопки форми', max_length=100, default='Отримати консультацію')
    contact_success_title = models.CharField('Заголовок після відправки', max_length=200, default='Дякуємо за звернення!')
    contact_success_text = models.CharField(
        'Текст після відправки', max_length=300,
        default='Наш менеджер зв\'яжеться з вами найближчим часом.',
    )

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'phone_main': '+38 (098) 123 45 67',
            'address': '',
        })
        return obj


class HeroSlide(models.Model):
    image = models.ImageField('Зображення', upload_to='hero/')
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Підзаголовок', max_length=300, blank=True)
    cta_text = models.CharField('Текст кнопки', max_length=100, default="Зв'язатися")
    cta_link = models.CharField('Посилання кнопки', max_length=200, default='#contacts')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд Hero'
        verbose_name_plural = 'Слайди Hero'

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField('Назва', max_length=200)
    short_description = models.TextField('Короткий опис', blank=True)
    icon_svg = models.TextField('SVG іконка', blank=True, help_text='Inline SVG код')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Завершений'),
        ('in_progress', 'В процесі'),
        ('planned', 'Запланований'),
    ]
    name = models.CharField('Назва', max_length=200)
    address = models.CharField('Адреса', max_length=300)
    city = models.CharField('Місто', max_length=100, default='м. Вишгород')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='completed')
    year_completed = models.PositiveIntegerField('Рік завершення', null=True, blank=True)
    floors = models.CharField('Поверхи', max_length=50)
    apartments_count = models.PositiveIntegerField('Кількість квартир', default=0)
    total_area = models.DecimalField('Загальна площа, м\u00b2', max_digits=12, decimal_places=2, default=0)
    commercial_area = models.DecimalField('Комерційні площі, м\u00b2', max_digits=10, decimal_places=2, default=0)
    description = models.TextField('Опис', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Об'єкт"
        verbose_name_plural = "Об'єкти"

    def __str__(self):
        return self.name

    @property
    def cover_image(self):
        img = self.images.filter(is_cover=True).first()
        if not img:
            img = self.images.first()
        return img


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images', verbose_name="Об'єкт"
    )
    image = models.ImageField('Зображення', upload_to='projects/')
    caption = models.CharField('Підпис', max_length=200, blank=True)
    is_cover = models.BooleanField('Обкладинка', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Фото об'єкта"
        verbose_name_plural = "Фото об'єктів"

    def __str__(self):
        return f'{self.project.name} - {self.caption or self.pk}'

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="max-height:80px;" />')
        return ''
    image_preview.short_description = 'Preview'


class Advantage(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    value = models.CharField('Значення', max_length=50, help_text='Напр. "930+" або "19"')
    description = models.CharField('Опис', max_length=200)
    icon_svg = models.TextField('SVG іконка', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self):
        return self.title


class WorkStep(models.Model):
    step_number = models.PositiveIntegerField('Номер кроку')
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Опис')
    icon_svg = models.TextField('SVG іконка', blank=True)

    class Meta:
        ordering = ['step_number']
        verbose_name = 'Крок роботи'
        verbose_name_plural = 'Кроки роботи'

    def __str__(self):
        return f'{self.step_number}. {self.title}'


class PartnerProject(models.Model):
    CATEGORY_CHOICES = [
        ('industrial', 'Промислове'),
        ('residential', 'Житлове'),
        ('commercial', 'Комерційне'),
        ('cottage', 'Котеджні містечка'),
    ]
    name = models.CharField('Назва проєкту', max_length=200)
    description = models.CharField('Опис', max_length=300, blank=True)
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES, default='industrial')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Партнерський проєкт'
        verbose_name_plural = 'Партнерські проєкти'

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('realized', 'Реалізовані об\'єкти'),
        ('completed', 'Об\'єкти Вишгород'),
        ('perspective', 'Перспективні проєкти'),
    ]
    image = models.ImageField('Зображення', upload_to='gallery/')
    caption = models.CharField('Підпис', max_length=200, blank=True)
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Об'єкт"
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Зображення галереї'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.caption or f'Зображення #{self.pk}'

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="max-height:80px;" />')
        return ''
    image_preview.short_description = 'Preview'


class PerspectiveInfo(models.Model):
    title = models.CharField('Назва', max_length=200, default='ЖК у м. Васильків')
    subtitle = models.CharField('Підзаголовок', max_length=300, blank=True)
    description = models.TextField('Опис')
    location = models.CharField('Локація', max_length=200, blank=True)
    hero_image = models.ImageField('Головне зображення', upload_to='perspectives/', blank=True)

    class Meta:
        verbose_name = 'Перспективний проєкт'
        verbose_name_plural = 'Перспективний проєкт'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'description': '',
        })
        return obj


class PerspectiveStat(models.Model):
    perspective = models.ForeignKey(
        PerspectiveInfo, on_delete=models.CASCADE, related_name='stats', verbose_name='Проєкт'
    )
    label = models.CharField('Назва', max_length=100)
    value = models.PositiveIntegerField('Значення')
    suffix = models.CharField('Суфікс', max_length=20, blank=True, help_text='м\u00b2, га, шт')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Статистика проєкту'
        verbose_name_plural = 'Статистика проєктів'

    def __str__(self):
        return f'{self.label}: {self.value}{self.suffix}'


class ContactRequest(models.Model):
    name = models.CharField("Ім'я", max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    object_type = models.CharField("Тип об'єкта", max_length=200, blank=True)
    message = models.TextField('Повідомлення', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} - {self.phone} ({self.created_at:%d.%m.%Y})'
