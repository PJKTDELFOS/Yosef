from django import forms
from perfil import models

#fazer os widgets, e labels, e todo resto necessario amanha domingo

class PerfilForm(forms.ModelForm):
    class Meta:
        model=models.cadastrofuncionario
        fields='__all__'




class Dependenteform(forms.ModelForm):
    funcionario=forms.ModelChoiceField(
        queryset=models.cadastrofuncionario.objects.all(),
        label="Funcionario",
        required=False,
        empty_label=None,
        disabled=True,
    )
    class Meta:
        model=models.dependente
        fields='__all__'
        exclude=['funcionario']


class Uniformes_epi_form(forms.ModelForm):
    funcionario = forms.ModelChoiceField(
        queryset=models.cadastrofuncionario.objects.all(),
        label="Funcionario",
        required=False,
        empty_label=None,
        disabled=True,
    )
    class Meta:
        model=models.uniformes_EPI
        fields='__all__'
        exclude = ['funcionario']


