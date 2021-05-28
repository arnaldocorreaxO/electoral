from core.base.models import Reporte
from config import settings
from pyreportjasper import PyReportJasper
from config import conn
from django.http import FileResponse



class JasperReportBase():
	report_dir	= ''
	report_name = ''
	report_title= ''
	filename 	= ''
	params = {}
	
	def __init__(self):
		self.input_file = '{report_dir}{report_name}.jrxml'.format(report_dir=settings.REPORTS_DIR,report_name=self.report_name)		
		self.output_file = '{report_dir}{report_name}'.format(report_dir=settings.REPORTS_DIR,report_name=self.report_name)			
		self.dbconn= conn.JASPER_PGSQL
		super(JasperReportBase, self).__init__()

	def get_report(self):
		pyreportjasper = PyReportJasper()
		pyreportjasper.config(
			self.input_file,
			self.output_file,
			db_connection=self.dbconn,
			output_formats=["pdf"],
			parameters=self.get_params(),
			locale='es_PY'
		)
		pyreportjasper.process_report()


	def get_params(self):
		"""
		Este metodo sera implementado por cada uno de nuestros reportes
		"""
		"""
			params es una variable local de get_params()
			self.params es un atributo de la clase 
			aca unimos los dos diccionarios con dict
		"""	
		params = {  'P_TITULO1': settings.REPORT_TITULO1,
                    'P_TITULO2': settings.REPORT_TITULO2,
                    'P_TITULO3': settings.REPORT_TITULO3,
					'P_REPORTE': self.report_title,
                    'P_RUTA': settings.REPORTS_DIR }

		return dict(params, **self.params)
		# raise NotImplementedError

	def render_to_response(self):
		self.get_report()
		filepath = self.output_file +'.pdf'
		return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


	


