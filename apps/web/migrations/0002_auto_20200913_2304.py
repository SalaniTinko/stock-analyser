# Generated by Django 3.0.7 on 2020-09-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freebie',
            name='counter',
            field=models.DateTimeField(default=0),
        ),
        migrations.AlterField(
            model_name='freebie',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]