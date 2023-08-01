# Generated by Django 4.2.2 on 2023-08-01 11:18

from django.db import migrations, models
import django.db.models.deletion
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.FloatField()),
                ('size', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Коробка',
                'verbose_name_plural': 'Коробки',
            },
        ),
        migrations.CreateModel(
            name='DeliveryNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='', max_length=150)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('article_list', models.TextField(blank=True, null=True)),
                ('provider', models.CharField(default='', max_length=150)),
            ],
            options={
                'verbose_name': 'Накладная',
                'verbose_name_plural': 'Накладные',
            },
        ),
        migrations.CreateModel(
            name='Flaw',
            fields=[
                ('id', models.PositiveBigIntegerField()),
                ('amount', models.FloatField()),
                ('datetime', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('decision', models.BooleanField(blank=True)),
            ],
            options={
                'verbose_name': 'Брак',
                'verbose_name_plural': 'Бракованные детали',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('article', models.CharField(max_length=250, primary_key=True, serialize=False, verbose_name='Артикул')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('units', models.CharField(max_length=20, verbose_name='Единицы измерения')),
                ('maximum', models.FloatField(blank=True, null=True, verbose_name='Максимум продукции')),
                ('minimum', models.FloatField(blank=True, null=True, verbose_name='Минимум продукцииё')),
                ('mass', models.FloatField(blank=True, null=True, verbose_name='Масса одного изделия')),
            ],
            options={
                'verbose_name': 'Номенклатура',
                'verbose_name_plural': 'Номенклатура',
            },
        ),
        migrations.CreateModel(
            name='ProductionStorage',
            fields=[
                ('title', models.CharField(default='', max_length=250, primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('units', models.CharField(default='', max_length=20)),
            ],
            options={
                'verbose_name': 'Склад производства',
                'verbose_name_plural': 'Склады производства',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('adress', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('x_cell_size', models.PositiveIntegerField(default=0)),
                ('y_cell_size', models.PositiveIntegerField(default=0)),
                ('z_cell_size', models.PositiveIntegerField(default=0)),
                ('x_cell_coord', models.PositiveIntegerField(default=0)),
                ('y_cell_coord', models.PositiveIntegerField(default=0)),
                ('z_cell_coord', models.PositiveIntegerField(default=0)),
                ('storage_name', models.CharField(max_length=60, validators=[main.validators.validate_no_spaces])),
                ('mass', models.PositiveIntegerField(default=700)),
                ('visualization_x', models.IntegerField(default=20)),
                ('visualization_y', models.IntegerField(default=20)),
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
            name='THD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('THD_number', models.PositiveIntegerField()),
                ('ip', models.CharField(max_length=250)),
                ('is_using', models.BooleanField(default=False)),
                ('is_comp', models.BooleanField(default=False)),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.worker')),
            ],
            options={
                'verbose_name': 'Номер ТСД',
                'verbose_name_plural': 'Номер ТСД',
            },
        ),
        migrations.CreateModel(
            name='TempCrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.FloatField()),
                ('size', models.CharField(max_length=80)),
                ('crate', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.crates')),
            ],
            options={
                'verbose_name': 'Временная коробка',
                'verbose_name_plural': 'Временные коробки',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('production_time', models.TimeField(verbose_name='Время производства')),
                ('nomenclatures', models.ManyToManyField(to='main.nomenclature', verbose_name='Содержимое спецификации')),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
            },
        ),
        migrations.AddConstraint(
            model_name='nomenclature',
            constraint=models.CheckConstraint(check=models.Q(('units__exact', 'кг'), ('units__exact', 'шт'), _connector='OR'), name='Значение единиц измерения необходимо указывать в килограммах или штуках в формате кг или шт'),
        ),
        migrations.AddConstraint(
            model_name='nomenclature',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('units__exact', 'шт'), ('mass__isnull', False)), ('units__exact', 'кг'), _connector='OR'), name='Если изделие измеряется поштучно необходимо указать массу одного изделия'),
        ),
        migrations.AddField(
            model_name='flaw',
            name='nomenclature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.nomenclature'),
        ),
        migrations.AddField(
            model_name='flaw',
            name='worker_add',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='worker_addition', to='main.worker'),
        ),
        migrations.AddField(
            model_name='flaw',
            name='worker_decision',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='worker_decision', to='main.worker'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.worker'),
        ),
        migrations.AddField(
            model_name='crates',
            name='cell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='crates', to='main.storage'),
        ),
        migrations.AddField(
            model_name='crates',
            name='nomenclature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.nomenclature'),
        ),
    ]
