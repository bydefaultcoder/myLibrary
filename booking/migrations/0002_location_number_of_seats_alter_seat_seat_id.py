# Generated by Django 5.1 on 2024-08-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='number_of_seats',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Seat No'),
        ),
    ]
