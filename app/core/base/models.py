from django.db import models
from crum import get_current_user
from config import settings

# Create your models here.
'''MODELO BASE'''
class ModeloBase(models.Model):
	# RefDets = RefDet.objects.filter(cod_referencia='ESTADO')
	# CAMPOS POR DEFECTO PARA TODOS LOS MODELOS
	usu_insercion = models.ForeignKey(settings.AUTH_USER_MODEL,db_column='usu_insercion',verbose_name='Creado por',on_delete=models.CASCADE,related_name='+')
	fec_insercion = models.DateTimeField(verbose_name='Fecha Creación',auto_now_add=True)
	usu_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL,db_column='usu_modificacion',verbose_name='Modificado por',on_delete=models.CASCADE,related_name='+')
	fec_modificacion = models.DateTimeField(verbose_name='Fecha Modificación',auto_now=True)
	activo = models.BooleanField(default=True)
	# estado = models.ForeignKey(RefDet,db_column='estado',on_delete=models.CASCADE,limit_choices_to={'referencia': 'ESTADO'},to_field='valor',default='A')

	def get_name_usu_insercion(self):
		return self.usu_insercion.first_name
	get_name_usu_insercion.short_description = 'Creado por'
	
	def get_name_usu_modificacion(self):
		return self.usu_modificacion.first_name
	get_name_usu_modificacion.short_description = 'Modificado por'

	'''SAVE'''
	def save(self, *args, **kwargs):
		user = get_current_user()
		print(user)
		if user and not user.pk:
			user = None
		# print(dir(self))
		if not self.usu_insercion_id:
			self.usu_insercion = user
		self.usu_modificacion = user
		super(ModeloBase, self).save(*args, **kwargs)

	class Meta:
		abstract = True

'''PARAMETROS GENERALES'''
class Parametro(ModeloBase):
	parametro = models.CharField(max_length=25, unique=True)
	descripcion = models.CharField(max_length=100, unique=True)
	valor = models.CharField(max_length=100)

	def __str__(self):
		return "%s - %s " % (self.parametro, self.valor)

	class Meta:
		ordering = ['parametro', ]
		db_table = 'base_parametro'
		verbose_name = 'Parametro'
		verbose_name_plural = 'Parametros'


'''MODULOS'''
class Modulo(ModeloBase):
	# id = models.CharField('Código',db_column='cod_modulo',max_length=2,primary_key=True)
	cod_modulo = models.CharField('Código',db_column='cod_modulo',max_length=2,unique=True)
	denominacion = models.CharField(max_length=100,unique=True)

	def __str__(self):
		return f"{self.cod_modulo} - {self.denominacion}"

	class Meta:
		ordering = ['id', ]
		db_table = 'base_modulo'
		verbose_name = 'modulo'
		verbose_name_plural = 'modulos'

'''REPORTES'''
# class Reporte(ModeloBase):
# 	nombre_reporte = models.CharField(max_length=100,unique=True)
# 	titulo_reporte = models.CharField(max_length=100)
# 	ruta_reporte = models.CharField(max_length=100,null=True,blank=True)
	
# 	def __str__(self):
# 		return f"{self.nombre_reporte} - {self.titulo_reporte}"

# 	class Meta:
# 		ordering = ['id', ]
# 		db_table = 'base_reporte'
# 		verbose_name = 'reporte'
# 		verbose_name_plural = 'reportes'
