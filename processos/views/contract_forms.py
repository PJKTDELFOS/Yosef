from time import localtime

from django import forms
from processos import models


class ContractForm(forms.ModelForm):
    processo_de_origem = forms.CharField(label='Processo de origem',
                                       widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model=models.Contratos
        fields=['contratante','objeto','numero'
                ,'seguro','seguradora','apolice',
                'tipo_documento','documentos','inicio',
                'vigencia','fim_contrato','valor_total'
                ,'observacoes',]
        labels={
            'contratante':'Contratante',
            'objeto':'Objeto',
            'numero':'Numero do contrato',
            'seguro':'Possui seguro',
            'seguradora':'seguradora',
            'apolicie':'apolice de seguro ',
            'tipo_documento':'Tipo do documento',
            'documento':'Inserir Documento',
            'inicio':'Inicio do Contrato',
            'vigencia':'vigencia do Contrato',
            'fim_contrato':'Fim do Contrato',
            'valor_total':'Valor Total',
            'observacoes':'observacoes',
            'total_executado':'Total Executado',
            'executavel':'Valor executavel',

            # TEM QUE SER O EQUIVALENTE NO MODELS PARA DATEFIELD
        }
        widgets={
            'inicio':forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
            'fim_contrato':forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
            'objeto':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder': 'Descreva o objeto'},
                                    ),
            'seguro':forms.Select(),
            'tipo_documento':forms.Select(),
            'observacoes':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder':'Observações...'},),


            }
    def __init__(self,*args,**kwargs):
        processo_obj=kwargs.pop('processo_de_origem',None)
        super().__init__(*args,**kwargs)
        if processo_obj:
            self.fields['processo_de_origem'].initial=processo_obj.numero_processo
            self.instance.processo=processo_obj
            self.fields['processo_de_origem'].label='Processo de origem'
        else:
            self.instance.processo=None
            self.fields['processo_de_origem'].initial='Nenhum processo selecionado'
















