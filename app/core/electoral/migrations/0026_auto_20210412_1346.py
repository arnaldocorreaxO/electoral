# Generated by Django 3.1.2 on 2021-04-12 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0025_elector_telefono'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departamento',
            options={'ordering': ['-id'], 'verbose_name': 'Departamento', 'verbose_name_plural': 'Departamentos'},
        ),
    ]
