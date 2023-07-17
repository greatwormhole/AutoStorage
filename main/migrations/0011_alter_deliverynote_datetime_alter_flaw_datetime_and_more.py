# Generated by Django 4.2.2 on 2023-07-17 11:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_worker_id_thd_worker_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverynote',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='flaw',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='storage',
            name='crate_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]
