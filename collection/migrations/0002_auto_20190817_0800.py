# Generated by Django 2.2.3 on 2019-08-17 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='gender',
            field=models.BooleanField(),
        ),
    ]
