# from core.utils import calculate_age
from django.db import models
from django.forms import model_to_dict
from core.electoral.utils import calculate_age
''' 
====================
=== DEPARTAMENTO ===
==================== '''
class Departamento(models.Model):
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        # default_permissions = ()
        # permissions = (
        #     ('view_departamento', 'Can view Departamento'),
        #     ('add_departamento', 'Can add Departamento'),
        #     ('change_departamento', 'Can change Departamento'),
        #     ('delete_departamento', 'Can delete Departamento'),
        # )
        ordering = ['denominacion']

class Distrito(models.Model):
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

class Seccional(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
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
        ordering = ['distrito','denominacion']


class Ciudad(models.Model):    
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

class Barrio(models.Model):    
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return self.denominacion
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'
        ordering = ['ciudad','denominacion']

class Manzana(models.Model): 
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)   
    cod = models.IntegerField()
    denominacion = models.CharField(max_length=50, verbose_name='Denominacion')

    def __str__(self):
        return f"{self.barrio} - {self.denominacion}"
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        unique_together=('cod','barrio')
        verbose_name = 'Manzana'
        verbose_name_plural = 'Manzanas'
        ordering = ['barrio','denominacion']

class Elector(models.Model):    
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
    voto1 = models.CharField(max_length=1,default='N')
    voto2 = models.CharField(max_length=1,default='N')
    voto3 = models.CharField(max_length=1,default='N')
    voto4 = models.CharField(max_length=1,default='N')
    voto5 = models.CharField(max_length=1,default='N')    
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
        item['barrio'] =  {'id':'','denominacion':''} if self.barrio is None else self.barrio.toJSON()
        item['manzana'] =  {'id':'','denominacion':''} if self.manzana is None else self.manzana.toJSON()        
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%Y-%m-%d')
        item['fecha_afiliacion'] = self.fecha_afiliacion.strftime('%Y-%m-%d')
        item['edad'] = self.get_edad()
        return item

    class Meta:
        verbose_name = 'Elector'
        verbose_name_plural = 'Electores'

class Padgral(models.Model):
    mesa = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=5, blank=True, null=True)
    numero_ced = models.DecimalField(unique=True, max_digits=15, decimal_places=0)
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
    cod_barrio = models.CharField(max_length=5, blank=True, null=True)
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
        # managed = False
        db_table = 'padgral'