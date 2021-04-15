# -*- codign: utf-8 -*-
import os
import uuid

from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms.models import model_to_dict

from config import settings


class User(AbstractUser):
    dni = models.CharField(max_length=13, unique=True, verbose_name='Cédula o RUC')
    image = models.ImageField(upload_to='users/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    is_change_password = models.BooleanField(default=False)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, default=uuid.uuid4, unique=True)

    def toJSON(self):
        item = model_to_dict(self, exclude=['last_login', 'token', 'password', 'user_permissions'])
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['groups'] = self.get_groups()
        item['last_login'] = None if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        return item

    def generate_token(self):
        return uuid.uuid4()

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

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(User, self).delete()

    def get_groups(self):
        data = []
        for i in self.groups.all():
            data.append({'id': i.id, 'name': i.name})
        return data

    def get_group_id_session(self):
        try:
            request = get_current_request()
            return int(request.session['group'].id)
        except:
            return 0

    def set_group_session(self):
        try:
            request = get_current_request()
            groups = request.user.groups.all()
            if groups:
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

    def create_or_update_password(self, password):
        try:
            if self.pk is None:
                self.set_password(password)
            else:
                user = User.objects.get(pk=self.pk)
                if user.password != password:
                    self.set_password(password)
        except:
            pass

    def is_client(self):
        try:
            if hasattr(self, 'client'):
                return True
        except Exception as e:
            print(e)
            pass
        return False

    def __str__(self):
        return self.get_full_name()
