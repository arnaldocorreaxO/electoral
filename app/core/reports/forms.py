from core.electoral.models import Barrio, LocalVotacion, Manzana, Operador, Seccional, TipoVoto
from django import forms

class ReportForm(forms.Form):
    local_votacion = forms.ChoiceField()
    seccional = forms.ChoiceField()
    barrio = forms.ChoiceField()
    manzana = forms.ChoiceField()
    tipo_voto = forms.ChoiceField()
    operador = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        # print(usuario)
        super().__init__(*args, **kwargs)  
        if usuario:
            self.fields['local_votacion'] = forms.ModelChoiceField(queryset=LocalVotacion.objects.filter(
                ciudad__distrito=usuario.distrito, activo=True).order_by('id'), empty_label="(Todos)")
            self.fields['seccional'] = forms.ModelChoiceField(queryset=Seccional.objects.filter(
                ciudad__distrito=usuario.distrito, activo=True).order_by('id'), empty_label="(Todos)")
            self.fields['barrio'] = forms.ModelChoiceField(queryset=Barrio.objects.filter(
                ciudad__distrito=usuario.distrito, activo=True).order_by('id'), empty_label="(Todos)")
            self.fields['manzana'] = forms.ModelChoiceField(queryset=Manzana.objects.filter(
                barrio__ciudad__distrito=usuario.distrito, activo=True).order_by('barrio__id','cod'), empty_label="(Todos)")
            self.fields['operador'] = forms.ModelChoiceField(queryset=Operador.objects.filter(
                distrito=usuario.distrito, activo=True).order_by('denominacion'), empty_label="(Todos)")
            self.fields['tipo_voto'] = forms.ModelChoiceField(
                queryset=TipoVoto.objects.filter(activo=True).order_by('id'), empty_label="(Todos)")

            #WIDGET
            self.fields['local_votacion'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})
            self.fields['seccional'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})
            self.fields['barrio'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})
            self.fields['manzana'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})   
            self.fields['tipo_voto'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})   
            self.fields['operador'].widget.attrs.update({'class': 'form-control select2','multiple':'true'})   
            
    # Extra Fields
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    salto_pagina = forms.BooleanField(initial=True,required=False)
    titulo_extra = forms.CharField(required=False)
    #WIDGET
    titulo_extra.widget.attrs.update({'class': 'form-control'})   