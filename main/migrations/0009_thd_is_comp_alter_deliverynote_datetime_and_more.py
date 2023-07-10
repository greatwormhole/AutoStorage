# Generated by Django 4.2.2 on 2023-07-10 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_deliverynote_datetime_alter_flaw_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='thd',
            name='is_comp',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deliverynote',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 10, 12, 38, 20, 611449)),
        ),
        migrations.AlterField(
            model_name='flaw',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 10, 12, 38, 20, 611449), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='thd',
            name='THD_number',
            field=models.PositiveIntegerField(),
        ),
    ]
