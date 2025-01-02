from django import forms
from processos import models


class PedidoForms(forms.ModelForm):
    contrato_de_origem=forms.CharField(label='Contrato de origem',
                                       widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model=models.Pedidos
        fields='__all__'
        exclude=['contrato','data_hora_att',]
        labels={
            'numero':'numero do pedido',
            'valor':'valor do pedido',
            'data_origem':'Data de origem',
            'cnpj_contratante':'CNPJ Contratante',
            'contratante':'Contratante',
            'empenho':'Empenho',
            'ordem_fornecimento':'Ordem Fornecimento',
            'recebimento_empenho':'Recebimento Empenho',
            'contato':'Nome do contato',
            'telefone':'Telefone',
            'email':'Email',
            'objeto':'Objeto do pedido',
            'data_entrega':'Data de entrega do pedido',
            'unidade_fornecimento':'Unidade Fornecimento',
            'qtde':'Quantidade',
            'coordenador':'Coordenador',
            'status':'Status',
            'tipo_documento':'Tipo Documento',
            'documentos':'Documento',
            'endereco_entrega':'Endereço de entrega',
            'observacoes':'observacoes',
        }
        widgets={
            'data_origem':forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
            'recebimento_empenho':forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
            'data_entrega':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),
            'observacoes':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder': 'Descreva observações ou '
                                                          'ocorrencias de importancia'},
                                    ),
            'objeto':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder': 'Descreva observações ou '
                                                          'ocorrencias de importancia'}),
            'status':forms.Select(attrs={'type':'select',}),
            'tipo_documento':forms.Select(attrs={'type':'select',}),
        }


    def clean_tipo_documento(self):
        tipo_documento = self.cleaned_data['tipo_documento']
        if not tipo_documento or tipo_documento == '':
            return 'PEDIDO'
        return tipo_documento

    def __init__(self, *args, **kwargs):
        contrato_obj = kwargs.pop('contrato_de_origem', None)
        super().__init__(*args, **kwargs)
        if contrato_obj:
            self.fields['contrato_de_origem'].initial = contrato_obj.numero
            self.instance.contrato = contrato_obj
            self.fields['contrato_de_origem'].label = 'Contrato de origem'
        else:
            self.instance.processo = None
            self.fields['contrato_de_origem'].initial = 'Nenhum contrato selecionado'



