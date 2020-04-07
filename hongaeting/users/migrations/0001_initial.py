# Generated by Django 2.2.9 on 2020-04-04 03:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('university_email', users.models.NullableEmailField(blank=True, help_text='학교 인증을 위한 메일', max_length=100, null=True, unique=True)),
                ('student_id_card_image', models.ImageField(blank=True, max_length=1000, null=True, upload_to=users.models.student_id_card_image_path)),
                ('is_confirmed_student', models.BooleanField(default=False, help_text='학교 인증을 받았는지 여부')),
                ('user_code', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=8, unique=True)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10)),
                ('born_year', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1980), users.models.max_value_current_year])),
                ('university', models.CharField(blank=True, choices=[('HONGIK', 'HONGIK'), ('KYUNGHEE', 'KYUNGHEE'), ('YONSEI', 'YONSEI')], max_length=10, null=True)),
                ('campus_location', models.CharField(choices=[('SEOUL', 'SEOUL'), ('INTERNATIONAL', 'INTERNATIONAL'), ('SINCHON', 'SINCHON')], max_length=20)),
                ('scholarly_status', models.CharField(choices=[('ATTENDING', 'ATTENDING'), ('TAKING_OFF', 'TAKING_OFF')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
