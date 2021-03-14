# Generated by Django 2.2 on 2020-06-08 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20200608_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='rating',
            field=models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='course',
            name='rating_count',
            field=models.PositiveIntegerField(default=149),
        ),
    ]
