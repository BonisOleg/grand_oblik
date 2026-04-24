from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from core.models import (
    SiteSettings, HeroSlide, Service, Project, ProjectImage,
    Advantage, WorkStep, PartnerProject, GalleryImage,
    PerspectiveInfo, PerspectiveStat,
)

SEED = settings.BASE_DIR / 'seed_media'


class Command(BaseCommand):
    help = 'Наповнює БД початковими даними ЕЛІТ-ФАСАД'

    def handle(self, *args, **options):
        self.seed_settings()
        self.seed_hero()
        self.seed_services()
        self.seed_projects()
        self.seed_advantages()
        self.seed_steps()
        self.seed_partners()
        self.seed_perspective()
        self.seed_gallery()
        self.stdout.write(self.style.SUCCESS('Дані успішно завантажені.'))

    def _save_image(self, field, rel_path, name):
        path = SEED / rel_path
        if path.exists():
            with open(path, 'rb') as f:
                field.save(name, File(f), save=False)
            return True
        self.stdout.write(self.style.WARNING(f'  Файл не знайдено: {path}'))
        return False

    def seed_settings(self):
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        s.company_name = 'ЕЛІТ-ФАСАД ГРУП'
        s.slogan = 'Будівництво та девелопмент з 2007 року'
        s.phone_main = '+38 (044) 561-62-63'
        s.phone_dev = '+38 (099) 352-20-01'
        s.email = 'elit.fasad.ltd@gmail.com'
        s.address = 'Київська обл., Вишгородський р-он, м. Вишгород, вул. Шолуденка, буд. 18А, оф.181'
        s.meta_title = 'ЕЛІТ-ФАСАД ГРУП — Будівництво житлових комплексів'
        s.meta_description = (
            'Група компаній ЕЛІТ-ФАСАД — будівництво багатоквартирних житлових будинків '
            'у Вишгороді та Київській області з 2007 року. Фасадні роботи, генпідряд, девелопмент.'
        )
        s.about_title = 'Про компанію'
        s.about_subtitle = 'Будівництво та девелопмент з 2007 року'
        s.about_text_1 = (
            'Група компаній ТОВ «ЕЛІТ-ФАСАД», ТОВ «ЕЛІТ-ФАСАД ГРУП», ТОВ «ЕЛІТ-ФАСАД ДЕВЕЛОПМЕНТ», '
            'ТОВ «ЕЛІТ-ФАСАД ЛТД», ТОВ «ВАН СТРОЙ ДЕВЕЛОПМЕНТ» та обслуговуюча організація '
            'ТОВ «ЗІРКА СЕРВІС ЕЛІТ» засновані на основі практичного досвіду реалізації будівельних '
            'проєктів у Києві та Київській області. Основними напрямами діяльності на початковому етапі '
            'були виконання комплексних фасадних робіт, монтаж металоконструкцій, комплексних ремонтних '
            'і реставраційних робіт. З часом цей досвід став фундаментом для розвитку компанії як '
            'повноцінного забудовника багатоквартирних житлових будинків. '
            'Початок діяльності у сфері девелопменту було закладено у червні 2007 року в місті Вишгород, '
            'відтоді основним пріоритетом залишається створення якісного житла, що поєднує сучасні '
            'будівельні рішення, комфорт і енергоефективність. Реалізовані об\'єкти забезпечили сотні '
            'сімей затишними оселями, які відповідають високим стандартам якості та дозволяють '
            'оптимізувати витрати на експлуатацію.'
        )
        s.about_text_2 = (
            'За роки роботи на будівельному ринку компанія досягла високого рівня професійної взаємодії '
            'з клієнтами та партнерами. Індивідуальний підхід до кожного проєкту та відповідальність у '
            'виконанні зобов\'язань дозволяють нам формувати довгострокові відносини, завдяки чому '
            'більшість клієнтів, партнерів і постачальників обирають співпрацю з нами на постійній основі. '
            'На підприємстві працюють кваліфіковані, досвідчені фахівці в сфері будівництва. '
            'Компанія ТОВ «ЕЛІТ-ФАСАД ГРУП» у 2023 році пройшла акредитацію UNGM та має реєстраційний '
            'номер акаунту #957086. '
            'Сьогодні група компаній — це надійний партнер у сфері будівництва, який об\'єднує досвід, '
            'відповідальність і орієнтацію на результат. Ми будуємо довгострокові відносини з клієнтами, '
            'партнерами та постачальниками, забезпечуючи індивідуальний підхід до кожного проєкту та '
            'бездоганну якість виконання робіт. '
            'Наша мета — створювати сучасний життєвий простір, у якому поєднуються комфорт, безпека та довіра.'
        )
        s.projects_title = "Власні об'єкти"
        s.projects_subtitle = 'Збудовані житлові комплекси'
        s.services_title = 'Наші послуги'
        s.experience_title = 'Наш досвід'
        s.experience_subtitle = 'Проєкти, в яких ми брали участь'
        s.gallery_title = 'Галерея'
        s.gallery_tab_realized = "Реалізовані об'єкти"
        s.gallery_tab_completed = 'Об\'єкти Вишгород'
        s.gallery_tab_perspective = 'Перспективні проєкти'
        s.contacts_title = 'Контакти'
        s.contacts_subtitle = "Залишилися питання? Зв'яжіться з нами"
        s.contact_form_text = 'Заповніть форму і наш менеджер зателефонує вам найближчим часом'
        s.contact_form_button = 'Отримати консультацію'
        s.contact_success_title = 'Дякуємо за звернення!'
        s.contact_success_text = "Наш менеджер зв'яжеться з вами найближчим часом."
        # Вбудована карта (output=embed) для вул. Котляревського, 3, Полтава
        s.google_maps_embed_url = (
            'https://maps.google.com/maps?q=%D0%B2%D1%83%D0%BB%D0%B8%D1%86%D1%8F+'
            '%D0%9A%D0%BE%D1%82%D0%BB%D1%8F%D1%80%D0%B5%D0%B2%D1%81%D1%8C%D0%BA%D0%BE%D0%B3%D0%BE%2C+3%2C+'
            '%D0%9F%D0%BE%D0%BB%D1%82%D0%B0%D0%B2%D0%B0&z=17&output=embed&hl=uk'
        )
        s.save()
        self.stdout.write('  SiteSettings OK')

    def seed_hero(self):
        if HeroSlide.objects.exists():
            return
        slide = HeroSlide(
            title='ЕЛІТ-ФАСАД ГРУП',
            subtitle='Будівництво та девелопмент з 2007 року',
            cta_text="Зв'язатися",
            cta_link='#contacts',
            order=0,
        )
        self._save_image(slide.image, 'hero/hero-main.jpg', 'hero-main.jpg')
        slide.save()
        self.stdout.write('  HeroSlide OK')

    def seed_services(self):
        if Service.objects.exists():
            return
        services = [
            ('Комплексні фасадні роботи', 'Вентиляційні алюмінієві фасади, утеплення, облицювання'),
            ('Монтаж металоконструкцій', 'Виготовлення та монтаж металевих каркасів і конструкцій'),
            ('Ремонтні та реставраційні роботи', 'Комплексний ремонт і реставрація будівель'),
            ('Будівництво житлових будинків', 'Генпідряд будівництва багатоквартирних будинків'),
            ('Проєктні та будівельно-монтажні роботи', 'Повний цикл від проєктування до здачі'),
            ('Промислове будівництво', 'Будівництво заводських, складських та офісних приміщень'),
        ]
        for i, (name, desc) in enumerate(services):
            Service.objects.create(name=name, short_description=desc, order=i)
        self.stdout.write('  Services OK')

    def seed_projects(self):
        if Project.objects.exists():
            return
        projects_data = [
            {
                'name': 'ЖК "Зірка Дніпра"', 'address': 'вул. Глібова, 43',
                'status': 'completed', 'year': 2013, 'floors': '10',
                'apts': 168, 'area': 17533.9, 'comm': 594.4,
                'images': ['zirka-dnipra.jpeg'],
            },
            {
                'name': 'ЖК "Зірка Вишгорода"', 'address': 'вул. Шолуденка, 18А',
                'status': 'completed', 'year': 2016, 'floors': '10',
                'apts': 184, 'area': 22740.77, 'comm': 775.73,
                'images': ['zirka-vyshgoroda.jpeg'],
            },
            {
                'name': 'ЖК "Зірковий"', 'address': 'вул. Ватутіна, 79',
                'status': 'completed', 'year': 2018, 'floors': '10',
                'apts': 196, 'area': 23014.16, 'comm': 809.28,
                'images': ['zirkovyi.jpeg'],
            },
            {
                'name': 'ЖК "Зіркова Вежа"', 'address': 'вул. Шолуденка, 26',
                'status': 'in_progress', 'year': None, 'floors': '10, 12',
                'apts': 382, 'area': 39375.37, 'comm': 1115.31,
                'images': ['zirkova-vezha-1.jpeg', 'zirkova-vezha-2.jpeg'],
            },
        ]
        for i, pd in enumerate(projects_data):
            proj = Project.objects.create(
                name=pd['name'], address=pd['address'], city='м. Вишгород',
                status=pd['status'], year_completed=pd['year'],
                floors=pd['floors'], apartments_count=pd['apts'],
                total_area=pd['area'], commercial_area=pd['comm'], order=i,
            )
            for j, img_name in enumerate(pd['images']):
                pi = ProjectImage(project=proj, is_cover=(j == 0), order=j)
                self._save_image(pi.image, f'projects/{img_name}', img_name)
                pi.save()
        self.stdout.write('  Projects OK')

    def seed_advantages(self):
        if Advantage.objects.exists():
            return
        advs = [
            ('Досвід', '19+', 'Років на ринку будівництва', 0),
            ('Квартири', '930+', 'Квартир побудовано та здано', 1),
            ('Якість', '100%', 'Індивідуальний підхід до кожного', 2),
        ]
        for title, val, desc, order in advs:
            Advantage.objects.create(title=title, value=val, description=desc, order=order)
        self.stdout.write('  Advantages OK')

    def seed_steps(self):
        if WorkStep.objects.exists():
            return
        steps = [
            (1, 'Консультація', 'Обговорюємо ваші потреби, бюджет та терміни'),
            (2, 'Проєктування', 'Розробляємо проєктну документацію та план робіт'),
            (3, 'Будівництво', 'Виконуємо роботи з контролем якості на кожному етапі'),
            (4, 'Здача', 'Здаємо об\'єкт в експлуатацію та передаємо власникам'),
        ]
        for num, title, desc in steps:
            WorkStep.objects.create(step_number=num, title=title, description=desc)
        self.stdout.write('  WorkSteps OK')

    def seed_partners(self):
        if PartnerProject.objects.exists():
            return
        partners = [
            ('Procter & Gamble Ukraine', 'Завод та автопарковка, м. Бориспіль', 'industrial'),
            ('ТРЦ Guliver', 'Підрядні роботи, центр Києва', 'commercial'),
            ('Інститут Шалімова', 'Алюмінієві вентиляційні фасади', 'commercial'),
            ('ЖК "Родинний Затишок"', 'Фасадні роботи', 'residential'),
            ('ЖК "Флагман"', 'Фасадні роботи', 'residential'),
            ('ТЦ "Мега Сіті"', 'Фасадні роботи', 'commercial'),
            ('ЖК "Перлина Троєщини"', 'Фасадні роботи, м. Київ', 'residential'),
            ('GK Алюпол', 'Офісні/складські будівлі, смт. Бородянка', 'industrial'),
            ('Завод "Стімекс"', 'ПВХ продукція та віконні системи', 'industrial'),
            ('Котеджне містечко', '', 'cottage'),
            ('Котеджне містечко', '', 'cottage'),
            ('', '', 'cottage'),
        ]
        for i, (name, desc, cat) in enumerate(partners):
            PartnerProject.objects.create(name=name, description=desc, category=cat, order=i)
        self.stdout.write('  PartnerProjects OK')

    def seed_perspective(self):
        if PerspectiveInfo.objects.filter(pk=1).exists() and PerspectiveInfo.objects.get(pk=1).description:
            return
        p, _ = PerspectiveInfo.objects.get_or_create(pk=1)
        p.title = 'ЖК у м. Васильків'
        p.subtitle = 'Унікальний проєкт комфорт класу в центрі міста'
        p.description = (
            'Ведуться організаційні роботи по новому будівельному майданчику в м. Васильків, '
            'Київської області. Це житловий комплекс, який являється унікальним проєктом комфорт '
            'класу та знаходиться в центрі міста. Комплекс займає 12 га та включає квартири двох типів, '
            'комерційні площі, дитячі садочки, ТРЦ та паркінги. Будинки передбачено збудувати з сучасних '
            'матеріалів з дотриманням енергозберігаючих технологій. Територія закрита, має цілодобовий '
            'пропускний пункт з охороною.'
        )
        p.location = 'м. Васильків, Київська область'
        self._save_image(p.hero_image, 'perspectives/16-poverkhovi.jpg', 'vasylkiv-panorama.jpg')
        p.save()

        PerspectiveStat.objects.filter(perspective=p).delete()
        stats = [
            ('Площа комплексу', 12, 'га', 0),
            ('Житлова площа', 164100, 'м²', 1),
            ('Комерційні площі', 12900, 'м²', 2),
            ('Паркомісця', 1750, '', 3),
        ]
        for label, val, suf, order in stats:
            PerspectiveStat.objects.create(perspective=p, label=label, value=val, suffix=suf, order=order)
        self.stdout.write('  PerspectiveInfo OK')

    def seed_gallery(self):
        if GalleryImage.objects.exists():
            return

        for proj in Project.objects.all():
            for pi in proj.images.all():
                GalleryImage.objects.create(
                    image=pi.image,
                    caption=proj.name,
                    category='completed',
                    project=proj,
                    order=GalleryImage.objects.count(),
                )

        perspective_images = [
            ('panorama.jpg', 'Панорама комплексу'),
            ('dvir.jpg', 'Двір та благоустрій'),
            ('vulychna.jpg', 'Вулична перспектива'),
            ('mizh-budynkamy.jpg', 'Перспектива між будинками'),
            ('balkony.jpg', 'Фасад з балконами'),
            ('16-poverkhovi.jpg', 'Панорама 16-поверхових будинків'),
            ('dytiachyi.jpg', 'Дитячий майданчик'),
            ('detali.jpg', 'Деталі фасаду'),
            ('z-vysoty.jpg', 'Вигляд з висоти пташиного польоту'),
        ]
        for fname, caption in perspective_images:
            gi = GalleryImage(
                caption=caption,
                category='perspective',
                order=GalleryImage.objects.count(),
            )
            self._save_image(gi.image, f'perspectives/{fname}', fname)
            gi.save()
        self.stdout.write('  Gallery OK')
