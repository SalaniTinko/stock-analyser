# Generated by Django 2.1.7 on 2019-03-21 12:18
from django.conf import settings
from django.db import migrations,models


def create_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get_or_create(
        id=settings.SITE_ID
    )[0]
    # strip leading http:// from site url since django sites framework doesn't expect it
    site.domain = settings.PROJECT_METADATA['URL'].replace('http://', '').replace('https://', '')
    site.name = settings.PROJECT_METADATA['NAME']
    site.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_site),
        migrations.CreateModel(
            name='Freebie',
            fields=[
            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip',models.GenericIPAddressField(auto_created=True,unique=True)), 
                 ('counter', models.IntegerField(default=0))
                 ]
                 )
        ]