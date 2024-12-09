from django import forms
from processos import models


class PedidoForms(forms.ModelForm):
    contrato=forms.ModelChoiceField(
        queryset=models.Contratos.objects.all(),
        label="Contrato",
        required=False,
        empty_label=None,
        disabled=True,
    )
    class Meta:
        model=models.Pedidos
        fields='__all__'
        exclude=['contrato','data_hora_att']
        labels={
            'contrato':'Contrato',
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
        contrato = kwargs.pop('contrato',None)
        super().__init__(*args, **kwargs)
        if contrato:
            self.fields['contrato'].initial =contrato



'''
 contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE, related_name='pedidos')
    numero=models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_origem=models.DateField(blank=True,null=True) ok
    cnpj_contratante=models.CharField(max_length=18,default='')
    contratante=models.CharField(max_length=60,default='')
    empenho=models.CharField(max_length=50,default='')
    ordem_fornecimento=models.CharField(max_length=50,blank=True,default='')
    recebimento_empenho=models.DateField(blank=True,null=True)
    contato=models.CharField(max_length=50,blank=True,default='')
    telefone=models.CharField(max_length=50,blank=True,default='')
    email=models.EmailField(max_length=50,default='')
    objeto=models.TextField(blank=True,max_length=600,default='')
    data_entrega=models.DateTimeField(blank=True,null=True)
    unidade_fornecimento=models.CharField(max_length=50,default='')
    qtde=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    coordenador=models.CharField(max_length=50,default='')
    show = models.BooleanField(default=True)
    status = models.CharField(default=None, max_length=25, choices=(
        ('RECEBIDO', 'PEDIDO RECEBIDO NA UNIDADE'),
        ('EM PRODUÇÃO', 'EM PRODUÇÃO'),
        ('EM EXECUÇÃO', 'SENDO PRESTADO(EXECUTADO)'),
        ('ENTREGUE', 'PEDIDO ENTREGUE'),
        ('FINALIZADO', 'OPERAÇÃO FINALIZADA'),
        ('EM ACEITE', 'AGUARDANDO APROVAÇÃO DO CLIENTE'),
        ('APROVADO', 'SERVIÇO OU PRODUTO APROVADO'),
        ('FATURADO', 'PARA EMITIR NOTA FISCAL'),
        ('NF EMITIDA', 'NF EMITIDA'),
        ('NF RETORNADA', 'NF RETORNADA POR ERRO'),
        ('NF PAGA', 'CLIENTE PAGOU'),
        ('FINALIZADO', 'PEDIDO FINALIZADO'),
    ))
    tipo_documento = models.CharField(default='PEDIDO', max_length=25, choices=(
        ('RELATORIOS', 'RELATORIOS'),
        ('PEDIDO', 'PEDIDO'),
        ('NOTAS REEMBOLSO', 'NOTAS DE REEMBOLSO'),
        ('NF PARA FATURA', 'NOTAS DE FATURAMENTO'),
        ('ACEITE', 'ACEITES'),
        ('DIVERSOS', 'ACEITES'),

    ))
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.pedido_upload_path,
        verbose_name="Documentos ", max_length=255,)
    endereco_entrega=models.TextField(blank=True,default='',max_length=1800)
    observacoes=models.TextField(blank=True,default='',max_length=1800)
    data_hora_att=models.DateTimeField(blank=True,null=True,auto_now=True,)
    
     
        para os de data fixa
        forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'}),
        para os de hora fixa e segura
        forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),
        
    
    
'''