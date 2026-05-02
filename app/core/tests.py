from config.wsgi import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.pos.models import *

dashboard = Dashboard()
dashboard.name = 'FACTORA POS'
dashboard.icon = 'fas fa-at'
dashboard.layout = 1
dashboard.card = ' '
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.brand_logo = ' '
dashboard.sidebar = 'sidebar-light-primary'
dashboard.save()

type = ModuleType()
type.name = 'Seguridad'
type.icon = 'fas fa-lock'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
	module.permits.add(p)	
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for p in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for p in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Administradores'
module.url = '/user/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los administradores del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Bodega'
type.icon = 'fas fa-boxes'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 2
module.name = 'Proveedores'
module.url = '/pos/scm/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck'
module.description = 'Permite administrar a los proveedores de las compras'
module.save()
for p in Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Categorías'
module.url = '/pos/scm/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las categorías de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Productos'
module.url = '/pos/scm/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los productos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Compras'
module.url = '/pos/scm/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dolly-flatbed'
module.description = 'Permite administrar las compras de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Ajuste de Stock'
module.url = '/pos/scm/product/stock/adjustment/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-sliders-h'
module.description = 'Permite administrar los ajustes de stock de productos'
module.save()
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Administrativo'
type.icon = 'fas fa-hand-holding-usd'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 3
module.name = 'Tipos de Gastos'
module.url = '/pos/frm/type/expense/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comments-dollar'
module.description = 'Permite administrar los tipos de gastos'
module.save()
for p in Permission.objects.filter(content_type__model=TypeExpense._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Gastos'
module.url = '/pos/frm/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-invoice-dollar'
module.description = 'Permite administrar los gastos de la compañia'
module.save()
for p in Permission.objects.filter(content_type__model=Expenses._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Cuentas por cobrar'
module.url = '/pos/frm/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-funnel-dollar'
module.description = 'Permite administrar las cuentas por cobrar de los clientes'
module.save()
for p in Permission.objects.filter(content_type__model=CtasCollect._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Cuentas por pagar'
module.url = '/pos/frm/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-money-check-alt'
module.description = 'Permite administrar las cuentas por pagar de los proveedores'
module.save()
for p in Permission.objects.filter(content_type__model=DebtsPay._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Facturación'
type.icon = 'fas fa-calculator'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 4
module.name = 'Clientes'
module.url = '/pos/crm/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-friends'
module.description = 'Permite administrar los clientes del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Ventas'
module.url = '/pos/crm/sale/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Ventas'
module.url = '/pos/crm/sale/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Promociones'
module.url = '/pos/crm/promotions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite administrar las promociones de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Promotions._meta.label.split('.')[1].lower()):
	module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Reportes'
type.icon = 'fas fa-chart-pie'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 5
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ventas'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Compras'
module.url = '/reports/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las compras'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Gastos'
module.url = '/reports/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los gastos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Cuentas por Pagar'
module.url = '/reports/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las cuentas por pagar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Cuentas por Cobrar'
module.url = '/reports/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las cuentas por cobrar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Perdidas y Ganacias'
module.url = '/reports/results/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de perdidas y ganancias'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Cambiar password'
module.url = '/user/admin/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/user/admin/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/crm/client/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Compañia'
module.url = '/pos/crm/company/update/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite gestionar la información de la compañia'
module.save()
print('insertado {}'.format(module.name))

group = Group()
group.name = 'Administrador'
group.save()
print('insertado {}'.format(group.name))
for m in Module.objects.filter().exclude(url__in=['/crm/client/update/profile/', '/pos/crm/sale/client/']):
	gm = GroupModule()
	gm.module = m
	gm.group = group
	gm.save()
	for perm in m.permits.all():
		group.permissions.add(perm)
		grouppermission = GroupPermission()
		grouppermission.module_id = m.id
		grouppermission.group_id = group.id
		grouppermission.permission_id = perm.id
		grouppermission.save()

group = Group()
group.name = 'Cliente'
group.save()
print('insertado {}'.format(group.name))
for m in Module.objects.filter(url__in=['/crm/client/update/profile/', '/pos/crm/sale/client/', '/user/admin/update/password/']).exclude():
	gm = GroupModule()
	gm.module = m
	gm.group = group
	gm.save()

u = User()
u.first_name = 'William Dávila'
u.last_name = 'Dávila Vargas'
u.username = 'admin'
u.dni = '0928363993'
u.email = 'davilawilliam93@gmail.com'
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.set_password('hacker94')
u.save()
group = Group.objects.get(pk=1)
u.groups.add(group)
