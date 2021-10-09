from core.electoral.models import Barrio, Elector, LocalVotacion, Manzana, Seccional, TipoVoto
from django import forms

class ReportForm(forms.Form):
    # Extra Fields
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    local_votacion = forms.ChoiceField(choices=[
    (item.id, item) for item in LocalVotacion.objects.filter(activo__exact=True).order_by('id')])
    seccional = forms.ChoiceField(choices=[
    (item.id, item) for item in Seccional.objects.filter(activo__exact=True).order_by('id')])
    barrio = forms.ChoiceField(choices=[
    (item.id, item ) for item in Barrio.objects.filter(activo__exact=True).order_by('id')])
    manzana = forms.ChoiceField(choices=[
    (item.id, item) for item in Manzana.objects.filter(activo__exact=True).order_by('barrio__id','cod')])
    tipo_voto = forms.ChoiceField(choices=[
    (item.id, item) for item in TipoVoto.objects.filter(activo__exact=True).order_by('id')])
    salto_pagina = forms.BooleanField(initial=True,required=False)
    titulo_extra = forms.CharField(required=False)

    local_votacion.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    seccional.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    barrio.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    manzana.widget.attrs.update({'class': 'form-control select2','multiple':'true'})   
    tipo_voto.widget.attrs.update({'class': 'form-control select2','multiple':'true'})   
    titulo_extra.widget.attrs.update({'class': 'form-control'})   
    