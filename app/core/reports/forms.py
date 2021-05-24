from core.electoral.models import Elector
from django import forms

class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class ReportFormElector001(forms.ModelForm):
    class Meta:
        model = Elector
        fields = ['barrio', 'manzana']
        widgets = {
            'barrio': forms.Select(attrs={'class': 'form-control select2', }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', }),
        }
