
import os


from django.test import TestCase
from pyreportjasper import PyReportJasper


# Create your tests here.
def processing():
	# REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__) + "/../"), 'reports')
	REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
	print(REPORTS_DIR)
	# JDBC_DIR = os.path.join(REPORTS_DIR,'sqlite-jdbc-3.34.0.jar')
	JDBC_DIR = os.path.join(REPORTS_DIR,'postgresql-42.2.20.jar')
	SQLITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'db.sqlite3')
	print(JDBC_DIR)
	print('jdbc:sqlite:'+SQLITE_DIR)
	input_file = os.path.join(REPORTS_DIR, 'rpt_001.jrxml')
	output_file = os.path.join(REPORTS_DIR, 'rpt_001')
	pyreportjasper = PyReportJasper()

	conn = {
			'driver'    : 'postgres',
			'username'  : 'postgres',
			'password'  : 'ox82',
			'host'      : 'localhost',
			'database'  : 'electoral',
			'schema'    : 'public',
			'port'      : '5432',
			'jdbc_driver':'org.postgresql.Driver',
			'jdbc_dir'  : JDBC_DIR
	}
	print(input_file)	

	params = {
            'P_BARRIO_ID': 2,
            'P_MANZANA_COD': None,
            'P_TITULO1': 'ASOCIACION NACIONAL REPUBLICANA',
            'P_TITULO2': '"PARTIDO COLORADO"',
            'P_REPORTE': 'MOVIMIENTO LISTA 6 "JOAQUINA INTENDENTA"',
            'P_RUTA': REPORTS_DIR,
        }

	print(params)
	pyreportjasper.config(
			input_file,
			output_file,
			db_connection=conn,			
			output_formats=["pdf", "xls"],
			parameters=params,
			locale='es_PY'
	)
	# output = pyreportjasper.list_report_params()
	# print(output)
	pyreportjasper.process_report()

processing()
