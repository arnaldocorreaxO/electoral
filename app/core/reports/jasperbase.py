from config import conn, settings
from crum import get_current_user
from django.http import FileResponse
from pyreportjasper import PyReportJasper
from core.user.models import User


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
		params = {  'P_TITULO1': settings.REPORT_TITULO1,
                    'P_TITULO2': settings.REPORT_TITULO2,
                    'P_TITULO3': settings.REPORT_TITULO3,
                    'P_TITULO4': self.report_title,
					'P_REPORTE': self.report_name,
					'P_USUARIO': str(get_current_user().username),
                    'P_RUTA': settings.REPORTS_DIR }
		# Concatenamos parametros locales y los enviados 
		return dict(params, **self.params)
		

	def render_to_response(self,tipo):
		# tipo = pdf, xls se refiere al tipo de archivo 
		self.get_report(tipo)
		filepath = self.output_file + f'.{tipo}'
		if tipo=='pdf':
			return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(filepath, 'rb'), content_type='application/vnd.ms-excel')
		

