# Generated by Django 3.2.5 on 2021-07-28 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20210728_0724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='occupancy_for_udult',
            new_name='occupancy_for_adult',
        ),
    ]
