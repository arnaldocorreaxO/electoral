# Generated by Django 3.1.2 on 2021-04-11 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0019_delete_manzana'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manzana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.IntegerField()),
                ('denominacion', models.CharField(max_length=50, verbose_name='Denominacion')),
                ('barrio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='electoral.barrio')),
            ],
            options={
                'verbose_name': 'Manzana',
                'verbose_name_plural': 'Manzanas',
                'ordering': ['-id'],
                'unique_together': {('cod', 'barrio')},
            },
        ),
    ]