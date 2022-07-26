# Generated by Django 4.0.6 on 2022-07-23 02:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='urgency',
            field=models.IntegerField(default=1, error_messages={'max_value': 'Please Choose an Urgency Between 1 and 10', 'min_value': 'Please Choose an Urgency Between 1 and 10'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Urgency (1-10)'),
        ),
    ]