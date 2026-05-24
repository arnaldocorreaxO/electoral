from core.base.utils import choiceNumbers
from core.electoral.models import (
    Barrio,
    Elector,
    LocalVotacion,
    Manzana,
    Operador,
    Seccional,
    TipoVoto,
)
from django import forms


class ReportForm(forms.Form):
    local_votacion = forms.ChoiceField()
    seccional = forms.ChoiceField()
    barrio = forms.ChoiceField()
    manzana = forms.ChoiceField()
    tipo_voto = forms.ChoiceField()
    operador = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario", None)
        # print(usuario)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields["local_votacion"] = forms.ModelChoiceField(
                queryset=LocalVotacion.objects.filter(
                    ciudad__distrito=usuario.distrito, activo=True
                ).order_by("id"),
                empty_label="(Todos)",
            )
            self.fields["seccional"] = forms.ModelChoiceField(
                queryset=Seccional.objects.filter(
                    ciudad__distrito=usuario.distrito, activo=True
                ).order_by("id"),
                empty_label="(Todos)",
            )
            self.fields["barrio"] = forms.ModelChoiceField(
                queryset=Barrio.objects.filter(
                    ciudad__distrito=usuario.distrito, activo=True
                ).order_by("id"),
                empty_label="(Todos)",
            )
            self.fields["manzana"] = forms.ModelChoiceField(
                queryset=Manzana.objects.filter(
                    barrio__ciudad__distrito=usuario.distrito, activo=True
                ).order_by("barrio__id", "cod"),
                empty_label="(Todos)",
            )
            self.fields["operador"] = forms.ModelChoiceField(
                queryset=Operador.objects.filter(
                    distrito=usuario.distrito, activo=True
                ).order_by("denominacion"),
                empty_label="(Todos)",
            )
            self.fields["tipo_voto"] = forms.ModelChoiceField(
                queryset=TipoVoto.objects.filter(activo=True).order_by("id"),
                empty_label="(Todos)",
            )

            # WIDGET
            self.fields["local_votacion"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )
            self.fields["seccional"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )
            self.fields["barrio"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )
            self.fields["manzana"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )
            self.fields["tipo_voto"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )
            self.fields["operador"].widget.attrs.update(
                {"class": "form-control select2", "multiple": "true"}
            )

    # Extra Fields
    date_range = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"})
    )

    salto_pagina = forms.BooleanField(initial=True, required=False)
    titulo_extra = forms.CharField(required=False)
    filas = forms.ChoiceField(choices=choiceNumbers(), initial=3)
    # WIDGET
    titulo_extra.widget.attrs.update({"class": "form-control"})
    # salto_pagina.widget.attrs.update({'class': 'form-control'})
    filas.widget.attrs.update({"class": "form-control select2"})


class FormFilterGenerarPDFMesa(forms.Form):
    # 1. DEFINICIÓN DE CAMPOS (Campos limpios sin congelamiento de memoria)
    local_votacion = forms.ChoiceField(label="Local de Votación")
    mesa = forms.ChoiceField(label="Mesa", required=False)

    TIPO_PLANILLA_CHOICES = [
        ("simple", "Simple (1 Cuadrícula Grande)"),
        ("doble", "Doble (Registro Votantes + Cantidad Votos)"),
    ]

    tipo_planilla = forms.ChoiceField(
        choices=TIPO_PLANILLA_CHOICES,
        initial="simple",
        widget=forms.Select(attrs={"class": "form-control select2"}),
        label="Tipo de Planilla",
    )

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario para poder filtrar por su distrito correspondiente
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

        # Opciones por defecto si no hay usuario o datos en el contexto
        self.fields["local_votacion"].choices = [("", "--- Seleccione Local ---")]
        self.fields["mesa"].choices = [("", "(Todas las Mesas)")]

        # --- 2. CARGA DINÁMICA DE OPCIONES (Evita congelamiento al reiniciar) ---
        if usuario:
            distrito = usuario.distrito

            # Carga de Locales de Votación filtrados por el distrito del usuario
            self.fields["local_votacion"].choices = [
                ("", "--- Seleccione Local ---")
            ] + [
                (item.id, str(item))
                for item in LocalVotacion.objects.filter(
                    ciudad__distrito=distrito, activo=True
                ).order_by(
                    "id"
                )  # Cambiado por id/denominacion según orden deseado
            ]

        # --- 3. APLICACIÓN AUTOMÁTICA DE ESTILOS BOOTSTRAP Y SELECT2 ---
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control select2", "style": "width: 100%;"}
            )
