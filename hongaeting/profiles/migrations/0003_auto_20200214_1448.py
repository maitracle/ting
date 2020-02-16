# Generated by Django 2.2.9 on 2020-02-14 05:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='appearance',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(120)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='hobby',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(120)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='ideal_type',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(120)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='last_tempting_word',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(120)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='personality',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(120)]),
            preserve_default=False,
        ),
    ]
