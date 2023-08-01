# Generated by Django 4.2.2 on 2023-08-01 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='plans',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Название плана'),
        ),
    ]
