from django.db import migrations

POLTAVA_MAP_URL = (
    'https://maps.google.com/maps'
    '?q=%D0%B2%D1%83%D0%BB%D0%B8%D1%86%D1%8F+'
    '%D0%9A%D0%BE%D1%82%D0%BB%D1%8F%D1%80%D0%B5%D0%B2%D1%81%D1%8C%D0%BA%D0%BE%D0%B3%D0%BE%2C+3%2C+'
    '%D0%9F%D0%BE%D0%BB%D1%82%D0%B0%D0%B2%D0%B0&z=17&output=embed&hl=uk'
)


def set_poltava_map_url(apps, schema_editor):
    """Replace any non-URL value (old iframe HTML or empty) with the Poltava embed URL."""
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for obj in SiteSettings.objects.all():
        current = obj.google_maps_embed_url or ''
        # Update if empty OR if the stored value is HTML (starts with '<')
        if not current.startswith('https://'):
            obj.google_maps_embed_url = POLTAVA_MAP_URL
            obj.save(update_fields=['google_maps_embed_url'])


def reverse_set_poltava_map_url(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_sitesettings_google_maps_help'),
    ]

    operations = [
        migrations.RunPython(
            set_poltava_map_url,
            reverse_set_poltava_map_url,
        ),
    ]
