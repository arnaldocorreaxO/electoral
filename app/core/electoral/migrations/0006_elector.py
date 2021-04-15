# Generated by Django 3.1.2 on 2021-04-06 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0005_auto_20210406_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.IntegerField()),
                ('apellido', models.CharField(max_length=120)),
                ('nombre', models.CharField(max_length=120)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('partido', models.CharField(blank=True, max_length=250, null=True)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_afiliacion', models.DateField()),
                ('voto1', models.CharField(default='N', max_length=1)),
                ('voto2', models.CharField(default='N', max_length=1)),
                ('voto3', models.CharField(default='N', max_length=1)),
                ('voto5', models.CharField(default='N', max_length=1)),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='electoral.departamento')),
                ('distrito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='electoral.distrito', to_field='cod')),
                ('seccional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='electoral.seccional', to_field='cod')),
            ],
            options={
                'verbose_name': 'Elector',
                'verbose_name_plural': 'Electores',
                'ordering': ['-id'],
            },
        ),
    ]
