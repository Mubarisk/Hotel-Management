# Generated by Django 3.2.5 on 2021-07-30 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('requested', 'requested'), ('booked', 'booked'), ('rejected', 'rejected'), ('delete', 'delete')], default='requested', max_length=30),
        ),
    ]
