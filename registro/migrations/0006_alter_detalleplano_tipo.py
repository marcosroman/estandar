# Generated by Django 4.0.5 on 2022-12-22 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0005_tipos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleplano',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.tipos'),
        ),
    ]