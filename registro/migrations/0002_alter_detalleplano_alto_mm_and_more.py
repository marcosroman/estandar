# Generated by Django 4.0.5 on 2022-12-20 13:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleplano',
            name='alto_mm',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(4000)]),
        ),
        migrations.AlterField(
            model_name='detalleplano',
            name='ancho_mm',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(4000)]),
        ),
        migrations.AlterField(
            model_name='detalleplano',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]