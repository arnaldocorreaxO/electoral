# Generated by Django 3.1.2 on 2021-04-11 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0021_padgral'),
    ]

    operations = [
        migrations.AddField(
            model_name='padgral',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='padgral',
            name='numero_ced',
            field=models.DecimalField(decimal_places=0, max_digits=15, unique=True),
        ),
    ]
