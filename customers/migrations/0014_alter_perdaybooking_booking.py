# Generated by Django 3.2.5 on 2021-08-04 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_perdaybooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perdaybooking',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perdaybooking', to='customers.booking'),
        ),
    ]
