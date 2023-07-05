# Generated by Django 4.2.2 on 2023-07-05 07:17

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('article', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('units', models.CharField(max_length=60)),
                ('maximum', models.FloatField(null=True)),
                ('minimum', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'Номенклатура',
                'verbose_name_plural': 'Номенклатура',
            },
        ),
        migrations.CreateModel(
            name='ProductionStorage',
            fields=[
                ('article', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
            ],
            options={
                'verbose_name': 'Склад производства',
                'verbose_name_plural': 'Склады производства',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('article_list', models.JSONField(default=dict, validators=[main.validators.ArticleJSONValidator(limit_value={'additionalProperties': False, 'properties': {'amount': {'type': 'number'}, 'article': {'type': 'string'}}, 'required': ['article', 'amount'], 'type': 'object'})])),
                ('production_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('adress', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('crate_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
                ('cell_size', models.CharField(max_length=60)),
                ('size_left', models.FloatField()),
                ('storage_name', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('storage_right', models.BooleanField()),
                ('plan_right', models.BooleanField()),
                ('quality_control_right', models.BooleanField()),
                ('status', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': 'Работники',
            },
        ),
        migrations.CreateModel(
            name='Flaw',
            fields=[
                ('id', models.PositiveBigIntegerField()),
                ('amount', models.FloatField()),
                ('datetime', models.DateTimeField(default=datetime.datetime(2023, 7, 5, 10, 17, 46, 305629), primary_key=True, serialize=False)),
                ('decision', models.BooleanField()),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.nomenclature')),
                ('worker_add', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='worker_addition', to='main.worker')),
                ('worker_decision', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='worker_decision', to='main.worker')),
            ],
            options={
                'verbose_name': 'Брак',
                'verbose_name_plural': 'Бракованные детали',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='DeliveryNote',
            fields=[
                ('number', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2023, 7, 5, 10, 17, 46, 305629))),
                ('article_list', models.JSONField(default=dict, validators=[main.validators.ArticleJSONValidator(limit_value={'additionalProperties': False, 'properties': {'amount': {'type': 'number'}, 'article': {'type': 'string'}}, 'required': ['article', 'amount'], 'type': 'object'})])),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.worker')),
            ],
            options={
                'verbose_name': 'Накладная',
                'verbose_name_plural': 'Накладные',
            },
        ),
        migrations.CreateModel(
            name='Crates',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('size', models.CharField(max_length=60)),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.nomenclature')),
            ],
            options={
                'verbose_name': 'Коробка',
                'verbose_name_plural': 'Коробки',
            },
        ),
    ]
