# Generated by Django 3.2.5 on 2021-08-04 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_alter_booking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerDayBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('live', 'live'), ('finished', 'finished')], default='pending', max_length=30)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.booking')),
            ],
        ),
    ]