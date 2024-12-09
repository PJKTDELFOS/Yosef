from time import localtime

from django import forms
from processos import models


class ContractForm(forms.ModelForm):
    processo=forms.ModelChoiceField(
        queryset=models.Processo.objects.all(),
        label='Processo de origem',
        required=False,
        empty_label=None,
        disabled=True,
    )
    class Meta:
        model=models.Contratos
        fields=['contratante','objeto','numero'
                ,'seguro','seguradora','apolice',
                'tipo_documento','documentos','inicio',
                'vigencia','fim_contrato','valor_total'
                ,'observacoes',]
        labels={
            'processo':'processo de origem',
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
    # def __init__(self, *args, **kwargs):
    #     processo = kwargs.pop('processo',None)
    #     super().__init__(*args, **kwargs)
    #     if processo:
    #         self.fields['processo'].initial =processo



    # def get_initial_for_field(self, field, field_name):
    #     field=models.Processo.objects.get(numero_processo=Processo.numero_processo)
    #     field_name='processo'
    #     value=getattr(field, field_name)
    #     return value














