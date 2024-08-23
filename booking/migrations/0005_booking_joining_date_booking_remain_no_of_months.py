# Generated by Django 4.2 on 2024-08-20 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_rename_monthly_prizing_monthlyplan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='joining_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='remain_no_of_months',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
