# Generated by Django 2.2.9 on 2020-04-30 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinhistory',
            name='message',
            field=models.CharField(max_length=200, verbose_name='포인트증감 메세지'),
        ),
        migrations.AlterField(
            model_name='coinhistory',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coin_histories', to='users.Profile', verbose_name='해당유저의 프로필'),
        ),
        migrations.AlterField(
            model_name='coinhistory',
            name='reason',
            field=models.CharField(choices=[('CONFIRM_USER', 'CONFIRM_USER'), ('SELF_DATE_PROFILE_VIEW', 'SELF_DATE_PROFILE_VIEW'), ('SELF_DATE_SEND_MESSAGE', 'SELF_DATE_SEND_MESSAGE')], max_length=50, verbose_name='포인트증감 이유'),
        ),
        migrations.AlterField(
            model_name='coinhistory',
            name='rest_coin',
            field=models.PositiveSmallIntegerField(verbose_name='남은 포인트'),
        ),
    ]
