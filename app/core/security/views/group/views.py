import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.security.forms import GroupForm
from core.security.mixins import PermissionMixin
from core.security.models import *


class GroupListView(PermissionMixin, TemplateView):
    template_name = 'group/list.html'
    permission_required = 'view_group'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for g in Group.objects.all():
                    data.append({
                        'id': g.id,
                        'name': g.name
                    })
            elif action == 'search_permissions':
                data = []
                group = Group.objects.get(pk=request.POST['id'])
                for i in group.permissions.all():
                    data.append({
                        'id': i.id,
                        'name': i.name,
                        'codename': i.codename,
                    })
            elif action == 'search_modules':
                data = []
                group = Group.objects.get(pk=request.POST['id'])
                for i in group.groupmodule_set.all():
                    data.append(i.module.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('group_create')
        context['title'] = 'Listado de Grupos'
        return context


class GroupCreateView(PermissionMixin, CreateView):
    model = Group
    template_name = 'group/create.html'
    form_class = GroupForm
    success_url = reverse_lazy('group_list')
    permission_required = 'add_group'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Group.objects.filter(name__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_modules(self):
        data = []
        for m in Module.objects.filter().order_by('name'):
            item = m.toJSON()
            item['state'] = 0
            data.append(item)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    groups_json = json.loads(request.POST['groups'])
                    group = Group()
                    group.name = request.POST['name']
                    group.save()
                    for m in groups_json:
                        groupmodule = GroupModule()
                        groupmodule.module_id = int(m['id'])
                        groupmodule.group_id = group.id
                        groupmodule.save()
                        permits = m['permits']
                        if len(permits):
                            for p in permits:
                                permission = Permission.objects.get(pk=p['id'])
                                group.permissions.add(permission)
                                grouppermission = GroupPermission()
                                grouppermission.group_id = group.id
                                grouppermission.module_id = groupmodule.module_id
                                grouppermission.permission_id = permission.id
                                grouppermission.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['modules'] = self.get_modules()
        context['title'] = 'Nuevo registro de un Grupo'
        context['action'] = 'add'
        return context


class GroupUpdateView(PermissionMixin, UpdateView):
    model = Group
    template_name = 'group/create.html'
    form_class = GroupForm
    success_url = reverse_lazy('group_list')
    permission_required = 'change_group'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Group.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_modules(self):
        data = []
        group = Group.objects.get(pk=self.get_object().id)
        for m in Module.objects.filter().exclude().order_by('name'):
            item = m.toJSON()
            item['state'] = 1 if group.groupmodule_set.filter(module_id=m.id).exists() else 0
            permits = []
            for p in m.permits.all():
                dict = {'id': p.id, 'name': p.name, 'codename': p.codename}
                dict['state'] = 1 if group.permissions.filter(id=p.id).exists() else 0
                permits.append(dict)
            item['permits'] = permits
            data.append(item)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    groups_json = json.loads(request.POST['groups'])
                    group = self.object
                    group.name = request.POST['name']
                    group.save()
                    group.grouppermission_set.all().delete()
                    group.groupmodule_set.all().delete()
                    group.permissions.clear()
                    for m in groups_json:
                        groupmodule = GroupModule()
                        groupmodule.module_id = int(m['id'])
                        groupmodule.group_id = group.id
                        groupmodule.save()
                        permits = m['permits']
                        if len(permits):
                            for p in permits:
                                permission = Permission.objects.get(pk=p['id'])
                                group.permissions.add(permission)
                                grouppermission = GroupPermission()
                                grouppermission.group_id = group.id
                                grouppermission.module_id = groupmodule.module_id
                                grouppermission.permission_id = permission.id
                                grouppermission.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['modules'] = self.get_modules()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Grupo'
        context['action'] = 'edit'
        return context


class GroupDeleteView(PermissionMixin, DeleteView):
    model = Group
    template_name = 'group/delete.html'
    success_url = reverse_lazy('group_list')
    permission_required = 'delete_group'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            group = self.get_object()
            group.groupmodule_set.all().delete()
            group.permissions.clear()
            group.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
