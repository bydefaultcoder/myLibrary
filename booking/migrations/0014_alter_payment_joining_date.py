# Generated by Django 5.1 on 2024-08-24 09:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_alter_payment_joining_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 24, 9, 6, 37, 88951, tzinfo=datetime.timezone.utc), verbose_name='Joining from'),
        ),
    ]
