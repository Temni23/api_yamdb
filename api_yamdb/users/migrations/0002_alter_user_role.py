# Generated by Django 3.2 on 2023-04-16 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default='user', max_length=255, verbose_name='Роль пользователя'),
        ),
    ]
