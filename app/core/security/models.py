import os
import socket
from datetime import *

from crum import get_current_request
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict

from config import settings
from core.security.choices import *
from core.user.models import User


class Dashboard(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    image = models.ImageField(verbose_name='Logo', upload_to='dashboard/%Y/%m/%d', null=True, blank=True)
    icon = models.CharField(max_length=50, verbose_name='Icono FontAwesome')
    layout = models.IntegerField(default=1, verbose_name='Diseño', blank=True, null=True, choices=layout_options)
    card = models.CharField(max_length=50, verbose_name='Card', choices=card, default=card[0][0])
    navbar = models.CharField(max_length=50, verbose_name='Navbar', choices=navbar, default=navbar[0][0])
    brand_logo = models.CharField(max_length=50, verbose_name='Brand Logo', choices=brand_logo,
                                  default=brand_logo[0][0])
    sidebar = models.CharField(max_length=50, verbose_name='Sidebar', choices=sidebar, default=sidebar[0][0])

    def __str__(self):
        return self.name

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-cubes'

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        default_permissions = ()
        permissions = (
            ('view_dashboard', 'Can view Dashboard'),
        )
        ordering = ['-id']


class ModuleType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    icon = models.CharField(max_length=100, unique=True, verbose_name='Icono')
    is_active = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_modules_vertical(self):
        listmodules = []
        try:
            request = get_current_request()
            group_id = request.user.get_group_id_session()
            if group_id != 0:
                listmodules = self.module_set.filter(is_active=True, is_vertical=True,
                                                     groupmodule__group_id=group_id).order_by('name')
        except:
            pass
        return listmodules

    def get_modules_horizontal(self):
        listmodules = []
        try:
            request = get_current_request()
            group_id = request.user.get_group_id_session()
            if group_id != 0:
                listmodules = self.module_set.filter(is_active=True, is_vertical=False,
                                                     groupmodule__group_id=group_id).order_by('name')
        except:
            pass
        return listmodules

    def toJSON(self):
        item = model_to_dict(self)
        item['icon'] = self.get_icon()
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    class Meta:
        verbose_name = 'Tipo de Módulo'
        verbose_name_plural = 'Tipos de Módulos'
        ordering = ['-name']


class Module(models.Model):
    url = models.CharField(max_length=100, verbose_name='Url', unique=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    moduletype = models.ForeignKey(ModuleType, null=True, blank=True, verbose_name='Tipo de Módulo',
                                   on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=100, verbose_name='Icono', null=True, blank=True)
    image = models.ImageField(upload_to='module/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    is_vertical = models.BooleanField(default=False, verbose_name='Vertical')
    is_active = models.BooleanField(default=True, verbose_name='Estado')
    is_visible = models.BooleanField(default=True, verbose_name='Visible')
    permits = models.ManyToManyField(Permission, verbose_name='Permisos', blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.url)

    def toJSON(self):
        item = model_to_dict(self)
        item['icon'] = self.get_icon()
        item['moduletype'] = {} if self.moduletype is None else self.moduletype.toJSON()
        item['icon'] = self.get_icon()
        item['image'] = self.get_image()
        item['permits'] = [{'id': p.id, 'name': p.name, 'codename': p.codename, 'state': 0} for p in self.permits.all()]
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'fa fa-times'

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def get_image_icon(self):
        if self.image:
            return self.get_image()
        if self.icon:
            return self.get_icon()
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def get_moduletype(self):
        if self.moduletype:
            return self.moduletype.name
        return None

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Module, self).delete()

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['-name']


class GroupModule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name = 'Grupo Módulo'
        verbose_name_plural = 'Grupos Módulos'
        default_permissions = ()
        ordering = ['-id']


class GroupPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name = 'Grupo Permiso'
        verbose_name_plural = 'Grupos Permisos'
        default_permissions = ()
        ordering = ['-id']


class DatabaseBackups(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    localhost = models.CharField(max_length=100, null=True, blank=True)
    hostname = models.TextField(default=socket.gethostname(), null=True, blank=True)
    archive = models.FileField(upload_to='backup/%Y/%m/%d')

    def __str__(self):
        return self.hostname

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['hour'] = self.hour.strftime('%H:%M %p')
        item['archive'] = self.get_archive()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.localhost = socket.gethostbyname(socket.gethostname())
        except:
            self.localhost = None
        super(DatabaseBackups, self).save()

    def get_archive(self):
        if self.archive:
            return '{0}{1}'.format(settings.MEDIA_URL, self.archive)
        return ''

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.archive.path)
        except:
            pass
        super(DatabaseBackups, self).delete()

    class Meta:
        verbose_name_plural = 'Respaldo de BD'
        verbose_name = 'Respaldos de BD'
        default_permissions = ()
        permissions = (
            ('view_databasebackups', 'Can view Respaldos de BD'),
            ('add_databasebackups', 'Can add Respaldos de BD'),
            ('delete_databasebackups', 'Can delete Respaldos de BD'),
        )
        ordering = ['-id']


class AccessUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    localhost = models.TextField()
    hostname = models.TextField(default=socket.gethostname())

    def __str__(self):
        return self.hostname

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['hour'] = self.hour.strftime('%H:%M %p')
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.localhost = socket.gethostbyname(socket.gethostname())
        except:
            self.localhost = None
        super(AccessUsers, self).save()

    class Meta:
        verbose_name = 'Acceso del usuario'
        verbose_name_plural = 'Accesos de los usuarios'
        default_permissions = ()
        permissions = (
            ('view_accessusers', 'Can view Acceso del usuario'),
            ('delete_accessusers', 'Can delete Acceso del usuario'),
        )
        ordering = ['-id']
