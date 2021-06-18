from core.electoral.models import Elector
from django import forms

class ReportForm(forms.ModelForm):
    # Extra Fields
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    class Meta:
        model = Elector
        fields = '__all__'
        widgets = {
            'local_votacion': forms.Select(attrs={'class': 'form-control select2', }),
            'seccional': forms.Select(attrs={'class': 'form-control select2', }),
            'barrio': forms.Select(attrs={'class': 'form-control select2', }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', }),
            'tipo_voto': forms.Select(attrs={'class': 'form-control select2', }),
        }
      
