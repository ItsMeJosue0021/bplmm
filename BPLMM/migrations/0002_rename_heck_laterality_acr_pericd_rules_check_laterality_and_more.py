# Generated by Django 5.0.3 on 2024-06-14 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BPLMM', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acr_pericd_rules',
            old_name='HECK_LATERALITY',
            new_name='CHECK_LATERALITY',
        ),
        migrations.RenameField(
            model_name='acr_pericd_rules_temp',
            old_name='HECK_LATERALITY',
            new_name='CHECK_LATERALITY',
        ),
    ]
