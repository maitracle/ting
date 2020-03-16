# Generated by Django 2.2.9 on 2020-03-13 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20200311_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_style',
            field=models.CharField(blank=True, max_length=1000, validators=[django.core.validators.MinLengthValidator(60)]),
        ),
    ]
