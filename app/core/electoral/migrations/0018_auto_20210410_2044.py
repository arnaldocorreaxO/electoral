# Generated by Django 3.1.2 on 2021-04-11 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0017_manzana_cod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manzana',
            name='cod',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='manzana',
            unique_together={('cod', 'barrio')},
        ),
    ]