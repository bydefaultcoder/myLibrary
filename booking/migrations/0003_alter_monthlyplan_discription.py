# Generated by Django 4.2 on 2024-09-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_monthlyplan_plan_of_time_alter_location_location_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyplan',
            name='discription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
