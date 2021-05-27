from core.electoral.models import Elector
from django import forms

class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    mesa = forms.ChoiceField(choices=[
    (item['mesa'], item['mesa']) for item in Elector.objects.values('mesa').extra(select={'int_mesa':'CAST(mesa AS INTEGER)'}).distinct().order_by('int_mesa')])


class ReportFormElector001(forms.ModelForm):
    class Meta:
        model = Elector
        fields = ['barrio', 'manzana']
        widgets = {
            'barrio': forms.Select(attrs={'class': 'form-control select2', }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', }),
        }
