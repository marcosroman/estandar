# Generated by Django 4.0.5 on 2022-07-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estandar',
            name='image',
        ),
        migrations.AddField(
            model_name='estandar',
            name='imagen',
            field=models.ImageField(default=1, upload_to='imagenes'),
            preserve_default=False,
        ),
    ]
