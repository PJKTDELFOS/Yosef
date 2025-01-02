from django import forms
from perfil.models import dependente,cadastrofuncionario,uniformes_EPI

class PerfilForm(forms.ModelForm):
    class Meta:
        model=cadastrofuncionario
        fields='__all__'
        labels={
            field.name: field.verbose_name.title() 
            for field in cadastrofuncionario._meta.get_fields()
            if hasattr(field, 'verbose_name')
        }
        widgets={
            'data_nascimento':forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
            'sexo':forms.Select(),
            'nacionalidade':forms.Select(),
            'estado_civil':forms.Select(),
            'formacao':forms.Select(),
            'setor':forms.Select(),
            'uf':forms.Select(),
            'ocorrencias':forms.Textarea(attrs={'rows':3}),
        }


class Dependenteform(forms.ModelForm):
    nome_funcionario = forms.CharField(label="Funcionário", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = dependente
        fields = ['nome_funcionario', 'nome_dependente', 'cpf_dependente', 'grau_relacional']

    def __init__(self, *args, **kwargs):
        funcionario_obj = kwargs.pop('nome_funcionario', None)
        super().__init__(*args, **kwargs)
        if funcionario_obj:
            self.fields['nome_funcionario'].initial = funcionario_obj.nomecompleto
            self.instance.funcionario = funcionario_obj
            self.fields['nome_funcionario'].label = "Funcionário"
        else:
            self.instance.funcionario = None
            self.fields['nome_funcionario'].initial = "Nenhum funcionário selecionado"

class Uniformes_epi_form(forms.ModelForm):
    nome_funcionario = forms.CharField(label="Funcionário", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model=uniformes_EPI
        fields='__all__'
        exclude = ['funcionario',]
        labels = {
            field.name: field.verbose_name.title()
            for field in uniformes_EPI._meta.get_fields()
            if hasattr(field, 'verbose_name')
        }
    def __init__(self, *args, **kwargs):
        funcionario_obj=kwargs.pop('nome_funcionario',None)
        super().__init__(*args,**kwargs)
        if funcionario_obj:
            self.fields['nome_funcionario'].initial=funcionario_obj.nomecompleto
            self.instance.funcionario=funcionario_obj
            self.fields['nome_funcionario'].label="Funcionario"
        else:
            self.instance.funcionario = None
            self.fields['nome_funcionario'].initial = "Nenhum funcionário selecionado"



