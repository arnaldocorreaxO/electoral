from config import conn, settings
from crum import get_current_user
from django.http import FileResponse
from django.db.models import Q
from pyreportjasper import PyReportJasper
from core.base.models import Parametro, Reporte



class JasperReportBase():
	report_dir	= '' #Directorio del reporte
	report_name = '' #Nombre fisico del reporte
	report_title= '' #Titulo Final del Reporte
	report_url	= '' #Url 
	filename 	= '' #Nombre archivo fisico
	params 		= {} #Diccionario de parametros del reporte 
	
	def __init__(self):		
		self.dbconn= conn.JASPER_PGSQL
		super(JasperReportBase, self).__init__()

	def get_report(self,tipo):
		self.input_file = '{report_dir}{report_name}.jrxml'.format(report_dir=settings.REPORTS_DIR,report_name=self.report_name)		
		self.output_file = '{report_dir}{report_name}'.format(report_dir=settings.REPORTS_DIR,report_name=self.report_name)			

		pyreportjasper = PyReportJasper()
		pyreportjasper.config(
			self.input_file,
			self.output_file,
			db_connection=self.dbconn,
			# tipo = pdf o xls
			output_formats=[tipo],
			parameters=self.get_params(),
			locale='es_PY'
		)
		pyreportjasper.process_report()

	def get_params(self):
		"""
		Este metodo sera implementado por cada uno de nuestros reportes
		"""	
		# PRIMERO ASIGNAMOS EL TITULO GENERAL DEL REPORTE Y LUEGO SI TIENE, EL TITULO ESPECIFICO
		reporte = Reporte.objects.filter(nombre=self.report_name).first()
		rptgral = Parametro.objects.filter(grupo__iexact='REPORTE_GENERAL')
		TITULO=[]
		TITULO.append(rptgral.filter(parametro__iexact='TR1').first().valor if rptgral.filter(parametro__iexact='TR1').first() else '')
		TITULO.append(rptgral.filter(parametro__iexact='TR2').first().valor if rptgral.filter(parametro__iexact='TR2').first() else '')
		TITULO.append(rptgral.filter(parametro__iexact='TR3').first().valor if rptgral.filter(parametro__iexact='TR3').first() else '')
		TITULO.append(rptgral.filter(parametro__iexact='TR4').first().valor if rptgral.filter(parametro__iexact='TR4').first() else '')

		if reporte:			
			TITULO[0] = reporte.titulo1 if reporte.titulo1 else TITULO[0]			
			TITULO[1] = reporte.titulo2 if reporte.titulo2 else TITULO[1]			
			TITULO[2] = reporte.titulo3 if reporte.titulo3 else TITULO[2]			
			TITULO[3] = reporte.titulo4 if reporte.titulo4 else TITULO[3]			

		params = {  'P_TITULO1': TITULO[0],					
                    'P_TITULO2': TITULO[1],                    
                    'P_TITULO3': TITULO[2],                    
                    'P_TITULO4': TITULO[3],                    
					'P_REPORTE': self.report_name,
					'P_USUARIO': str(get_current_user().username),
                    'P_RUTA': settings.REPORTS_DIR }
		
		return dict(params, **self.params)
		

	def render_to_response(self,tipo):
		# tipo = pdf, xls se refiere al tipo de archivo 
		self.get_report(tipo)
		filepath = self.output_file + f'.{tipo}'
		if tipo=='pdf':
			return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(filepath, 'rb'), content_type='application/vnd.ms-excel')
		

