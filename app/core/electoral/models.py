# from core.utils import calculate_age
from core.base.models import ModeloBase
from django.db import models
from django.forms import model_to_dict
from core.electoral.utils import calculate_age

''' 
====================
===    PAIS      ===
==================== '''
class Pais(ModeloBase):
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['denominacion']
''' 
====================
=== DEPARTAMENTO ===
==================== '''
class Departamento(ModeloBase):
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['denominacion']
''' 
====================
===   DISTRITO   ===
==================== '''
class Distrito(ModeloBase):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    cod = models.IntegerField(null=False, unique=True)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion    

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['departamento','denominacion']

''' 
====================
===    CIUDAD    ===
==================== '''
class Ciudad(ModeloBase):
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT,null=True,blank=True)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['denominacion']

''' 
====================
===    BARRIO    ===
==================== '''
class Barrio(ModeloBase):    
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def fullname(self):
        return f"({self.pk}) - {self.denominacion}" 
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'
        ordering = ['ciudad','denominacion']
''' 
====================
===   MANZANA    ===
==================== '''
class Manzana(ModeloBase): 
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)   
    cod = models.IntegerField()
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return f"{self.denominacion} - {self.barrio}"
    
    def fullname(self):
        return f"({self.barrio.pk} / {self.cod}) - {self.denominacion}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        unique_together=('cod','barrio')
        verbose_name = 'Manzana'
        verbose_name_plural = 'Manzanas'
        ordering = ['barrio','denominacion']

''' 
====================
===  SECCIONAL   ===
==================== '''
class Seccional(ModeloBase):
    # distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    cod = models.IntegerField(null=False, unique=True)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return f"{self.cod} - {self.denominacion}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Seccional'
        verbose_name_plural = 'Seccionales'
        ordering = ['ciudad','denominacion']


''' 
=========================
===  LOCAL VOTACION   ===
========================= '''
class LocalVotacion(ModeloBase):
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return f"{self.id} - {self.denominacion}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        # db_table = 'local_votacion'
        verbose_name = 'Local Votacion'
        verbose_name_plural = 'Locales de Votacion'
        ordering = ['ciudad','denominacion']

''' 
====================
=== TIPO DE VOTO ===
==================== '''
class TipoVoto(ModeloBase):
    cod = models.CharField(max_length=3,null=False, unique=True)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return f"{self.cod} - {self.denominacion}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo Voto'
        verbose_name_plural = 'Tipo de Votos'
        ordering = ['id','denominacion']


''' 
====================
===   ELECTOR    ===
==================== '''
class Elector(ModeloBase):    
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,null=True, blank=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT,null=True, blank=True)
    seccional = models.ForeignKey(Seccional, on_delete=models.PROTECT,null=True, blank=True)
    mesa = models.CharField(max_length=5, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    ci = models.IntegerField(null=True)
    apellido = models.CharField(max_length=120)
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=250,null=True, blank=True)
    partido = models.CharField(max_length=250,null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_afiliacion = models.DateField(null=True, blank=True)
    tipo_voto = models.ForeignKey(TipoVoto,related_name="tipo_voto", on_delete=models.PROTECT,null=True, blank=True)
    voto1 = models.CharField(max_length=1,default='N')
    voto2 = models.CharField(max_length=1,default='N')
    voto3 = models.CharField(max_length=1,default='N')
    voto4 = models.CharField(max_length=1,default='N')
    voto5 = models.CharField(max_length=1,default='N')
    local_votacion = models.ForeignKey(LocalVotacion, on_delete=models.PROTECT,null=True, blank=True)    
    pasoxpc = models.CharField(max_length=1,default='N')    
    pasoxmv = models.CharField(max_length=1,default='N')    
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT,null=True,blank=True) 
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT,null=True,blank=True) 
    manzana = models.ForeignKey(Manzana, on_delete=models.PROTECT,null=True,blank=True) 
    nro_casa = models.IntegerField(null=True,blank=True)
    telefono = models.CharField(max_length=120,null=True,blank=True)    

    def __str__(self):
        return f"{self.apellido} {self.nombre}"
       
    def get_edad(self):
        return calculate_age(self.fecha_nacimiento)

    def toJSON(self):
        item = model_to_dict(self,exclude=[''])
        item['fullname'] = str(self) #Retorna el metodo __str__ al hacer la conversion
        item['barrio'] = self.barrio.toJSON() if self.barrio  else {'id':'','denominacion':''}
        item['manzana'] = self.manzana.toJSON() if self.manzana else {'id':'','denominacion':''}
        item['tipo_voto'] = self.tipo_voto.toJSON() if self.tipo_voto else {'id':'','cod':''}
        item['barrio_fullname'] = self.barrio.fullname() if self.barrio else None
        item['manzana_fullname'] = self.manzana.fullname() if self.manzana else None
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%d/%m/%Y')
        item['fecha_afiliacion'] = self.fecha_afiliacion.strftime('%d/%m/%Y') 
        item['fec_modificacion'] = self.fec_modificacion.strftime('%d/%m/%Y %H:%M:%S')       
        item['edad'] = self.get_edad()
        return item

    class Meta:
        verbose_name = 'Elector'
        verbose_name_plural = 'Electores'
        ordering = ['id']


class PreElector(models.Model):    
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,null=True, blank=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT,null=True, blank=True)
    seccional = models.ForeignKey(Seccional, on_delete=models.PROTECT,null=True, blank=True)
    ci = models.IntegerField(null=True)
    apellido = models.CharField(max_length=120)
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=250,null=True, blank=True)
    partido = models.CharField(max_length=250,null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_afiliacion = models.DateField(null=True, blank=True)
    tipo_voto = models.ForeignKey(TipoVoto,related_name="pre_tipo_voto", on_delete=models.PROTECT,null=True, blank=True)
    voto1 = models.CharField(max_length=1,default='N')
    voto2 = models.CharField(max_length=1,default='N')
    voto3 = models.CharField(max_length=1,default='N')
    voto4 = models.CharField(max_length=1,default='N')
    voto5 = models.CharField(max_length=1,default='N')    
    pasoxpc = models.CharField(max_length=1,default='N')    
    pasoxmv = models.CharField(max_length=1,default='N')    
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT,null=True,blank=True) 
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT,null=True,blank=True) 
    manzana = models.ForeignKey(Manzana, on_delete=models.PROTECT,null=True,blank=True) 
    nro_casa = models.IntegerField(null=True,blank=True)
    telefono = models.CharField(max_length=120,null=True,blank=True)
    

    def __str__(self):
        return f"{self.apellido} {self.nombre}"

    class Meta:
        verbose_name = 'Pre-Elector'
        verbose_name_plural = 'Pre-Electores'
        ordering = ['id']


''' 
====================
===   PADGRAL    ===
==================== '''
# class Padgral(models.Model):
#     mesa = models.CharField(max_length=3, blank=True, null=True)
#     orden = models.CharField(max_length=5, blank=True, null=True)
#     numero_ced = models.DecimalField(unique=True, max_digits=15, decimal_places=0)
#     apellido = models.CharField(max_length=80, blank=True, null=True)
#     nombre = models.CharField(max_length=80, blank=True, null=True)
#     fecha_naci = models.DateField(blank=True, null=True)
#     direccion = models.CharField(max_length=200, blank=True, null=True)
#     estado = models.CharField(max_length=1, blank=True, null=True)
#     n_partido = models.CharField(max_length=200, blank=True, null=True)
#     cod_seccional = models.CharField(max_length=3, blank=True, null=True)
#     voto_19 = models.CharField(max_length=1, blank=True, null=True)
#     voto_23 = models.CharField(max_length=1, blank=True, null=True)
#     voto_1911 = models.CharField(max_length=1, blank=True, null=True)
#     voto_1612 = models.CharField(max_length=1, blank=True, null=True)
#     cod_barrio = models.CharField(max_length=5, blank=True, null=True)
#     cod_manzana = models.CharField(max_length=5, blank=True, null=True)
#     nro_casa = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
#     cod_lugar = models.CharField(max_length=5, blank=True, null=True)
#     voto = models.CharField(max_length=1, blank=True, null=True)
#     nro_telefono = models.CharField(max_length=50, blank=True, null=True)
#     referencia = models.CharField(max_length=50, blank=True, null=True)
#     pasoxpc = models.CharField(max_length=1, blank=True, null=True)
#     pasoxmv = models.CharField(max_length=1, blank=True, null=True)
#     cod_dpto = models.CharField(max_length=2, blank=True, null=True)
#     cod_dist = models.CharField(max_length=3, blank=True, null=True)
#     codigo_sex = models.CharField(max_length=1, blank=True, null=True)
#     voto_2003 = models.CharField(max_length=1, blank=True, null=True)

#     class Meta:
#         # managed = False
#         db_table = 'padgral'

class Padgral(models.Model):
    mesa = models.CharField(max_length=5, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    codigo_sec = models.CharField(max_length=5, blank=True, null=True)
    slocal = models.CharField(max_length=5, blank=True, null=True)
    apellido = models.CharField(max_length=250, blank=True, null=True)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    fecha_naci = models.CharField(max_length=20, blank=True, null=True)
    cod_dpto = models.CharField(max_length=5, blank=True, null=True)
    cod_dist = models.CharField(max_length=5, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    numero_cas = models.CharField(max_length=25, blank=True, null=True)
    codigo_sex = models.CharField(max_length=5, blank=True, null=True)
    fecha_afil = models.CharField(max_length=20, blank=True, null=True)
    dep_05 = models.CharField(max_length=5, blank=True, null=True)
    dis_05 = models.CharField(max_length=5, blank=True, null=True)
    zon_05 = models.CharField(max_length=5, blank=True, null=True)
    loc_05 = models.CharField(max_length=5, blank=True, null=True)
    partido = models.CharField(max_length=250, blank=True, null=True)
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
    numero_ced = models.DecimalField(unique=True, max_digits=50, decimal_places=0)
    nacional = models.CharField(max_length=5, blank=True, null=True)
    voto_2003 = models.CharField(max_length=5, blank=True, null=True)
    voto_19 = models.CharField(max_length=5, blank=True, null=True)
    voto_23 = models.CharField(max_length=5, blank=True, null=True)
    voto_1911 = models.CharField(max_length=5, blank=True, null=True)
    voto_1612 = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'padgral'