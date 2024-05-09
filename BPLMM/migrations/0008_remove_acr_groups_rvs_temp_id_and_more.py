# Generated by Django 5.0.3 on 2024-05-09 08:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPLMM', '0007_alter_acr_groups_icds_acr_groupid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acr_groups_rvs_temp',
            name='id',
        ),
        migrations.AddField(
            model_name='acr_groups_rvs_temp',
            name='RVSCODE',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
