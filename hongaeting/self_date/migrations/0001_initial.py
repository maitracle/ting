# Generated by Django 2.2.9 on 2020-04-28 06:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import self_date.models
import self_date.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coins', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfDateProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=8, unique=True)),
                ('height', models.PositiveSmallIntegerField()),
                ('body_type', models.CharField(choices=[('SLIM', 'SLIM'), ('SLIM_TONED', 'SLIM_TONED'), ('NORMAL', 'NORMAL'), ('BUFF', 'BUFF'), ('CHUBBY', 'CHUBBY')], max_length=10)),
                ('religion', models.CharField(choices=[('NOTHING', 'NOTHING'), ('CHRISTIANITY', 'CHRISTIANITY'), ('BUDDHISM', 'BUDDHISM'), ('CATHOLIC', 'CATHOLIC'), ('ETC', 'ETC')], max_length=20)),
                ('is_smoke', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=10)),
                ('tags', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, max_length=1000, null=True, upload_to=self_date.models.image_path)),
                ('one_sentence', models.CharField(max_length=35)),
                ('appearance', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(120)])),
                ('personality', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(120)])),
                ('hobby', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(120)])),
                ('date_style', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(60)])),
                ('ideal_type', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(120)])),
                ('chat_link', models.URLField(validators=[self_date.validators.chat_link_validator])),
                ('is_active', models.BooleanField(default=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelfDateProfileRight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('right_type', models.CharField(choices=[('CONFIRM_USER', 'CONFIRM_USER'), ('SELF_DATE_PROFILE_VIEW', 'SELF_DATE_PROFILE_VIEW'), ('SELF_DATE_SEND_MESSAGE', 'SELF_DATE_SEND_MESSAGE')], max_length=50)),
                ('buying_self_date_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buying_self_date_rights', to='self_date.SelfDateProfile')),
                ('coin_history', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='coins.CoinHistory')),
                ('target_self_date_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_self_date_rights', to='self_date.SelfDateProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelfDateLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_self_date_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_self_date_profile', to='self_date.SelfDateProfile')),
                ('self_date_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='self_date.SelfDateProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
