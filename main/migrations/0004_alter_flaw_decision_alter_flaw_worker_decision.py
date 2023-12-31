# Generated by Django 4.2.2 on 2023-08-09 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_flaw_id_remove_flaw_worker_add_rejectionact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flaw',
            name='decision',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flaw',
            name='worker_decision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='worker_decision', to='main.worker'),
        ),
    ]
