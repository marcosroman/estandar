# Generated by Django 4.0.5 on 2022-12-13 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0004_alter_estandar_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estandar',
            name='imagen',
            field=models.ImageField(upload_to='estandar'),
        ),
    ]
