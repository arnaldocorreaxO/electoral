# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Padgral(models.Model):
    mesa = models.CharField(max_length=5, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    codigo_sec = models.CharField(max_length=5, blank=True, null=True)
    slocal = models.CharField(max_length=5, blank=True, null=True)
    apellido = models.CharField(max_length=-1, blank=True, null=True)
    nombre = models.CharField(max_length=-1, blank=True, null=True)
    fecha_naci = models.CharField(max_length=20, blank=True, null=True)
    cod_dpto = models.CharField(max_length=5, blank=True, null=True)
    cod_dist = models.CharField(max_length=5, blank=True, null=True)
    direccion = models.CharField(max_length=-1, blank=True, null=True)
    numero_cas = models.CharField(max_length=25, blank=True, null=True)
    codigo_sex = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.CharField(max_length=20, blank=True, null=True)
    dep_05 = models.CharField(max_length=5, blank=True, null=True)
    dis_05 = models.CharField(max_length=5, blank=True, null=True)
    zon_05 = models.CharField(max_length=5, blank=True, null=True)
    loc_05 = models.CharField(max_length=5, blank=True, null=True)
    partido = models.CharField(max_length=-1, blank=True, null=True)
    key_dds = models.CharField(max_length=25, blank=True, null=True)
    key_dd = models.CharField(max_length=15, blank=True, null=True)
    key_ddz = models.CharField(max_length=15, blank=True, null=True)
    key_ddzl = models.CharField(max_length=15, blank=True, null=True)
    voto1 = models.CharField(max_length=5, blank=True, null=True)
    voto2 = models.CharField(max_length=5, blank=True, null=True)
    voto3 = models.CharField(max_length=5, blank=True, null=True)
    voto4 = models.CharField(max_length=5, blank=True, null=True)
    voto5 = models.CharField(max_length=5, blank=True, null=True)
    ced_ape = models.CharField(max_length=15, blank=True, null=True)
    sec_loc = models.CharField(max_length=15, blank=True, null=True)
    cod_barrio = models.CharField(max_length=5, blank=True, null=True)
    cod_manzana = models.CharField(max_length=5, blank=True, null=True)
    nro_casa = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cod_lugar = models.CharField(max_length=5, blank=True, null=True)
    voto = models.CharField(max_length=5, blank=True, null=True)
    pasoxpc = models.CharField(max_length=1, blank=True, null=True)
    pasoxmv = models.CharField(max_length=1, blank=True, null=True)
    cod_seccional = models.CharField(max_length=15, blank=True, null=True)
    estado = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.DecimalField(primary_key=True, max_digits=50, decimal_places=0)
    nacional = models.CharField(max_length=5, blank=True, null=True)
    voto_2003 = models.CharField(max_length=5, blank=True, null=True)
    voto_19 = models.CharField(max_length=5, blank=True, null=True)
    voto_23 = models.CharField(max_length=5, blank=True, null=True)
    voto_1911 = models.CharField(max_length=5, blank=True, null=True)
    voto_1612 = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padgral'
