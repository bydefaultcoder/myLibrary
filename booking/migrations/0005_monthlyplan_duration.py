# Generated by Django 4.2 on 2024-09-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_remove_monthlyplan_plan_of_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyplan',
            name='duration',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
