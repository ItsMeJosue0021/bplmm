# Generated by Django 5.0.3 on 2024-05-09 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPLMM', '0006_acr_groups_created_at_acr_groups_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acr_groups_icds',
            name='ACR_GROUPID',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='acr_groups_icds_temp',
            name='ACR_GROUPID',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='acr_groups_rvs',
            name='ACR_GROUPID',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='acr_groups_rvs_temp',
            name='ACR_GROUPID',
            field=models.CharField(max_length=255),
        ),
    ]
