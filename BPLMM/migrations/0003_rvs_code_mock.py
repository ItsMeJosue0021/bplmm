# Generated by Django 5.0.3 on 2024-05-07 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPLMM', '0002_alter_acr_groups_icds_temp_icdcode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RVS_CODE_MOCK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODE', models.CharField(max_length=255)),
            ],
        ),
    ]
