# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bsbardfn(models.Model):
    cod_barrio = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsbardfn'


class Bsciudfn(models.Model):
    cod_ciudad = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    abreviatura = models.CharField(max_length=3, blank=True, null=True)
    cod_pais = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsciudfn'


class Bsdisdfn(models.Model):
    cod_distrito = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsdisdfn'


class Bsdptdfn(models.Model):
    cod_dpto = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsdptdfn'


class Bsmdldfn(models.Model):
    cod_modulo = models.CharField(primary_key=True, max_length=2)
    descripcion = models.CharField(max_length=30)
    orden = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsmdldfn'


class Bsmnzdfn(models.Model):
    cod_barrio = models.OneToOneField(Bsbardfn, models.DO_NOTHING, db_column='cod_barrio', primary_key=True)
    cod_manzana = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bsmnzdfn'
        unique_together = (('cod_barrio', 'cod_manzana'),)


class Bspaidfn(models.Model):
    cod_pais = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    abreviatura = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bspaidfn'


class Bspxgdfn(models.Model):
    cod_modulo = models.CharField(primary_key=True, max_length=2)
    parametro = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    valor = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bspxgdfn'
        unique_together = (('cod_modulo', 'parametro'),)


class Bssecdfn(models.Model):
    cod_seccional = models.CharField(primary_key=True, max_length=5)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bssecdfn'


class Dummy(models.Model):
    x = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'dummy'


class Pad158(models.Model):
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.CharField(max_length=15, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.DateField(blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    codigo_sec = models.CharField(max_length=3, blank=True, null=True)
    slocal = models.CharField(max_length=3, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero_cas = models.CharField(max_length=10, blank=True, null=True)
    codigo_sex = models.CharField(max_length=2, blank=True, null=True)
    codigo_nac = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.DateField(blank=True, null=True)
    habilitado = models.CharField(max_length=3, blank=True, null=True)
    rcp_ok_05 = models.CharField(max_length=3, blank=True, null=True)
    anr_c = models.CharField(max_length=3, blank=True, null=True)
    dep_05 = models.CharField(max_length=3, blank=True, null=True)
    dis_05 = models.CharField(max_length=3, blank=True, null=True)
    zon_05 = models.CharField(max_length=3, blank=True, null=True)
    loc_05 = models.CharField(max_length=3, blank=True, null=True)
    sec_pos = models.CharField(max_length=3, blank=True, null=True)
    x_marca = models.CharField(max_length=3, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    key_dds = models.CharField(max_length=1, blank=True, null=True)
    key_dd = models.CharField(max_length=1, blank=True, null=True)
    key_ddz = models.CharField(max_length=1, blank=True, null=True)
    key_ddzl = models.CharField(max_length=1, blank=True, null=True)
    voto_19 = models.CharField(max_length=1, blank=True, null=True)
    voto_23 = models.CharField(max_length=1, blank=True, null=True)
    voto_1911 = models.CharField(max_length=1, blank=True, null=True)
    rcp_habil = models.CharField(max_length=1, blank=True, null=True)
    aprx = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pad158'


class Pad2008(models.Model):
    mesa = models.CharField(max_length=5, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    n_cedula = models.CharField(primary_key=True, max_length=15)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    n_partido = models.CharField(max_length=200, blank=True, null=True)
    fecnac = models.CharField(max_length=30, blank=True, null=True)
    seccional = models.CharField(max_length=5, blank=True, null=True)
    voto_19 = models.CharField(max_length=5, blank=True, null=True)
    voto_23 = models.CharField(max_length=5, blank=True, null=True)
    voto_1911 = models.CharField(max_length=5, blank=True, null=True)
    voto_1612 = models.CharField(max_length=5, blank=True, null=True)
    cod_barrio = models.CharField(max_length=5, blank=True, null=True)
    cod_manzana = models.CharField(max_length=5, blank=True, null=True)
    cod_ciudad = models.CharField(max_length=3, blank=True, null=True)
    cod_lugar = models.CharField(max_length=5, blank=True, null=True)
    voto = models.CharField(max_length=1, blank=True, null=True)
    nro_telefono = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    pasoxpc = models.CharField(max_length=1, blank=True, null=True)
    pasoxmv = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pad2008'


class Pad216(models.Model):
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.CharField(max_length=15, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.DateField(blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    codigo_sec = models.CharField(max_length=3, blank=True, null=True)
    slocal = models.CharField(max_length=3, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero_cas = models.CharField(max_length=10, blank=True, null=True)
    codigo_sex = models.CharField(max_length=2, blank=True, null=True)
    codigo_nac = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.DateField(blank=True, null=True)
    habilitado = models.CharField(max_length=3, blank=True, null=True)
    rcp_ok_05 = models.CharField(max_length=3, blank=True, null=True)
    anr_c = models.CharField(max_length=3, blank=True, null=True)
    dep_05 = models.CharField(max_length=3, blank=True, null=True)
    dis_05 = models.CharField(max_length=3, blank=True, null=True)
    zon_05 = models.CharField(max_length=3, blank=True, null=True)
    loc_05 = models.CharField(max_length=3, blank=True, null=True)
    sec_pos = models.CharField(max_length=3, blank=True, null=True)
    x_marca = models.CharField(max_length=3, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    key_dds = models.CharField(max_length=1, blank=True, null=True)
    key_dd = models.CharField(max_length=1, blank=True, null=True)
    key_ddz = models.CharField(max_length=1, blank=True, null=True)
    key_ddzl = models.CharField(max_length=1, blank=True, null=True)
    voto_19 = models.CharField(max_length=1, blank=True, null=True)
    voto_23 = models.CharField(max_length=1, blank=True, null=True)
    voto_1911 = models.CharField(max_length=1, blank=True, null=True)
    rcp_habil = models.CharField(max_length=1, blank=True, null=True)
    aprx = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pad216'


class Pad389(models.Model):
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.CharField(max_length=15, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.DateField(blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    codigo_sec = models.CharField(max_length=3, blank=True, null=True)
    slocal = models.CharField(max_length=3, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero_cas = models.CharField(max_length=10, blank=True, null=True)
    codigo_sex = models.CharField(max_length=2, blank=True, null=True)
    codigo_nac = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.DateField(blank=True, null=True)
    habilitado = models.CharField(max_length=3, blank=True, null=True)
    rcp_ok_05 = models.CharField(max_length=3, blank=True, null=True)
    anr_c = models.CharField(max_length=3, blank=True, null=True)
    dep_05 = models.CharField(max_length=3, blank=True, null=True)
    dis_05 = models.CharField(max_length=3, blank=True, null=True)
    zon_05 = models.CharField(max_length=3, blank=True, null=True)
    loc_05 = models.CharField(max_length=3, blank=True, null=True)
    sec_pos = models.CharField(max_length=3, blank=True, null=True)
    x_marca = models.CharField(max_length=3, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    key_dds = models.CharField(max_length=1, blank=True, null=True)
    key_dd = models.CharField(max_length=1, blank=True, null=True)
    key_ddz = models.CharField(max_length=1, blank=True, null=True)
    key_ddzl = models.CharField(max_length=1, blank=True, null=True)
    voto_19 = models.CharField(max_length=1, blank=True, null=True)
    voto_23 = models.CharField(max_length=1, blank=True, null=True)
    voto_1911 = models.CharField(max_length=1, blank=True, null=True)
    rcp_habil = models.CharField(max_length=1, blank=True, null=True)
    aprx = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pad389'


class Padgral(models.Model):
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.DecimalField(primary_key=True, max_digits=15, decimal_places=0)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    n_partido = models.CharField(max_length=200, blank=True, null=True)
    cod_seccional = models.CharField(max_length=3, blank=True, null=True)
    voto_19 = models.CharField(max_length=1, blank=True, null=True)
    voto_23 = models.CharField(max_length=1, blank=True, null=True)
    voto_1911 = models.CharField(max_length=1, blank=True, null=True)
    voto_1612 = models.CharField(max_length=1, blank=True, null=True)
    cod_barrio = models.ForeignKey(Bsmnzdfn, models.DO_NOTHING, db_column='cod_barrio', blank=True, null=True)
    cod_manzana = models.CharField(max_length=5, blank=True, null=True)
    nro_casa = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cod_lugar = models.CharField(max_length=5, blank=True, null=True)
    voto = models.CharField(max_length=1, blank=True, null=True)
    nro_telefono = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    pasoxpc = models.CharField(max_length=1, blank=True, null=True)
    pasoxmv = models.CharField(max_length=1, blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    codigo_sex = models.CharField(max_length=1, blank=True, null=True)
    voto_2003 = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padgral'


class Padsl2008(models.Model):
    mesa = models.CharField(max_length=5, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    n_cedula = models.CharField(primary_key=True, max_length=15)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    n_partido = models.CharField(max_length=200, blank=True, null=True)
    fecnac = models.CharField(max_length=30, blank=True, null=True)
    seccional = models.CharField(max_length=5, blank=True, null=True)
    voto_19 = models.CharField(max_length=5, blank=True, null=True)
    voto_23 = models.CharField(max_length=5, blank=True, null=True)
    voto_1911 = models.CharField(max_length=5, blank=True, null=True)
    voto_1612 = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padsl2008'


class Padtmp(models.Model):
    numero_ced = models.CharField(max_length=15)
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ce = models.CharField(max_length=15, blank=True, null=True)
    codigo_sec = models.CharField(max_length=3, blank=True, null=True)
    slocal = models.CharField(max_length=3, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.CharField(max_length=15, blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero_cas = models.CharField(max_length=10, blank=True, null=True)
    codigo_sex = models.CharField(max_length=2, blank=True, null=True)
    fecha_afil = models.CharField(max_length=15, blank=True, null=True)
    key_slocal = models.CharField(max_length=5, blank=True, null=True)
    habilitado = models.CharField(max_length=3, blank=True, null=True)
    rcp_ok_05 = models.CharField(max_length=3, blank=True, null=True)
    anr_c = models.CharField(max_length=3, blank=True, null=True)
    dep_05 = models.CharField(max_length=3, blank=True, null=True)
    dis_05 = models.CharField(max_length=3, blank=True, null=True)
    zon_05 = models.CharField(max_length=3, blank=True, null=True)
    loc_05 = models.CharField(max_length=3, blank=True, null=True)
    sec_pos_vi = models.CharField(max_length=3, blank=True, null=True)
    sec_pos = models.CharField(max_length=3, blank=True, null=True)
    x_marca = models.CharField(max_length=3, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    key_dds = models.CharField(max_length=10, blank=True, null=True)
    key_dd = models.CharField(max_length=10, blank=True, null=True)
    key_ddz = models.CharField(max_length=10, blank=True, null=True)
    key_ddzl = models.CharField(max_length=10, blank=True, null=True)
    rcp_talon = models.CharField(max_length=10, blank=True, null=True)
    rcp_boleta = models.CharField(max_length=10, blank=True, null=True)
    rcp_fecins = models.CharField(max_length=15, blank=True, null=True)
    voto_19 = models.CharField(max_length=10, blank=True, null=True)
    voto_23 = models.CharField(max_length=10, blank=True, null=True)
    voto_1911 = models.CharField(max_length=10, blank=True, null=True)
    sec_loc = models.CharField(max_length=5, blank=True, null=True)
    civico = models.CharField(max_length=10, blank=True, null=True)
    cod_seccional = models.CharField(max_length=5, blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    cod_barrio = models.CharField(max_length=5, blank=True, null=True)
    cod_manzana = models.CharField(max_length=5, blank=True, null=True)
    voto_16 = models.CharField(max_length=10, blank=True, null=True)
    nro_casa = models.CharField(max_length=5, blank=True, null=True)
    cod_ciudad = models.CharField(max_length=3, blank=True, null=True)
    cod_lugar = models.CharField(max_length=5, blank=True, null=True)
    voto = models.CharField(max_length=10, blank=True, null=True)
    nro_telefono = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    pasoxpc = models.CharField(max_length=10, blank=True, null=True)
    pasoxmv = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padtmp'


class Prepadgral(models.Model):
    numero_ced = models.DecimalField(primary_key=True, max_digits=15, decimal_places=0)
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ce = models.CharField(max_length=15, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    fecha_naci = models.DateField(blank=True, null=True)
    cod_dpto = models.CharField(max_length=2, blank=True, null=True)
    cod_dist = models.CharField(max_length=3, blank=True, null=True)
    codigo_sec = models.CharField(max_length=3, blank=True, null=True)
    slocal = models.CharField(max_length=3, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero_cas = models.CharField(max_length=10, blank=True, null=True)
    codigo_sex = models.CharField(max_length=2, blank=True, null=True)
    codigo_nac = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.DateField(blank=True, null=True)
    habilitado = models.CharField(max_length=3, blank=True, null=True)
    rcp_ok_05 = models.CharField(max_length=3, blank=True, null=True)
    anr_c = models.CharField(max_length=3, blank=True, null=True)
    dep_05 = models.CharField(max_length=3, blank=True, null=True)
    dis_05 = models.CharField(max_length=3, blank=True, null=True)
    zon_05 = models.CharField(max_length=3, blank=True, null=True)
    loc_05 = models.CharField(max_length=3, blank=True, null=True)
    sec_pos = models.CharField(max_length=3, blank=True, null=True)
    x_marca = models.CharField(max_length=3, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    key_dds = models.CharField(max_length=1, blank=True, null=True)
    key_dd = models.CharField(max_length=1, blank=True, null=True)
    key_ddz = models.CharField(max_length=1, blank=True, null=True)
    key_ddzl = models.CharField(max_length=1, blank=True, null=True)
    voto_19 = models.CharField(max_length=1, blank=True, null=True)
    voto_23 = models.CharField(max_length=1, blank=True, null=True)
    voto_1911 = models.CharField(max_length=1, blank=True, null=True)
    rcp_habil = models.CharField(max_length=1, blank=True, null=True)
    aprx = models.CharField(max_length=1, blank=True, null=True)
    cod_seccional = models.CharField(max_length=5, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    cod_barrio = models.ForeignKey(Bsmnzdfn, models.DO_NOTHING, db_column='cod_barrio', blank=True, null=True)
    cod_manzana = models.CharField(max_length=5, blank=True, null=True)
    voto_16 = models.CharField(max_length=1, blank=True, null=True)
    nro_casa = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cod_ciudad = models.CharField(max_length=3, blank=True, null=True)
    cod_lugar = models.CharField(max_length=5, blank=True, null=True)
    voto = models.CharField(max_length=1, blank=True, null=True)
    nro_telefono = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    pasoxpc = models.CharField(max_length=1, blank=True, null=True)
    pasoxmv = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prepadgral'


class Puestocontrol(models.Model):
    numero_ced = models.DecimalField(primary_key=True, max_digits=15, decimal_places=0)
    nro_mesa = models.CharField(max_length=3, blank=True, null=True)
    nro_orden = models.CharField(max_length=5, blank=True, null=True)
    nro_ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puestocontrol'


class Regcivtmp(models.Model):
    depart = models.CharField(max_length=2, blank=True, null=True)
    distrito = models.CharField(max_length=2, blank=True, null=True)
    zona = models.CharField(max_length=3, blank=True, null=True)
    local = models.CharField(max_length=3, blank=True, null=True)
    talon = models.CharField(max_length=10, blank=True, null=True)
    boleta = models.CharField(max_length=10, blank=True, null=True)
    fec_inscri = models.CharField(max_length=15, blank=True, null=True)
    cedula = models.CharField(max_length=25, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    fec_nac = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    sexo = models.CharField(max_length=2, blank=True, null=True)
    nacional = models.CharField(max_length=5, blank=True, null=True)
    part = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regcivtmp'


class Regpart(models.Model):
    cod = models.CharField(max_length=5, blank=True, null=True)
    descrip = models.CharField(max_length=80, blank=True, null=True)
    siglas = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regpart'


class Votos2003(models.Model):
    numero_ced = models.DecimalField(max_digits=22, decimal_places=0, blank=True, null=True)
    voto_2003 = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'votos_2003'
