# from django import forms
# from processos import models
#
#
# class ContractForm(forms.ModelForm):
#     class Meta:
#         model=models.Contratos
#         fields='__all__'
#         labels={
#             'processo':'Processo de origem',
#             'contratante':'Contratante',
#             'objeto':'Objeto',
#             'numero':'Numero do contrato',
#             'seguro':'Possui seguro',
#             'seguradora':'seguradora',
#             'apolicie':'apolice de seguro ',
#             'tipo_documento':'Tipo do documento',
#             'documento':'Inserir Documento',
#             'inicio':'Inicio do Contrato',
#             'vigencia':'vigencia do Contrato',
#             'fim_contrato':'Fim do Contrato',
#             'valor_total':'Valor Total',
#             'observacoes':'observacoes',
#
#         }
#         widgets={
#             'inicio':forms.DateInput(attrs={'type':'date'}),
#             'fim_contrato':forms.DateInput(attrs={'type':'date'}),
#             'objeto':forms.Textarea(attrs={'type':'textarea',
#                                            'rows':5,
#                                            'placeholder': 'Descreva as ocorrências...'},
#                                     ),
#             'seguro':forms.Select(),
#             'tipo_documento':forms.Select(),
#             'observacoes':forms.Textarea(attrs={'type':'textarea',
#                                            'rows':5,
#                                            'placeholder':'Observações...'},)
#
#
#             }
#
#         def __init__(self, *args, **kwargs):
#             processo=kwargs.get('instance',None)
#             if processo and processo.processo:
#                 pass



'''
lado campo:lado nome
  processo = models.ForeignKey(Processo, on_delete=models.CASCADE, blank=False, null=False,related_name='contratos')
    contratante=models.CharField(max_length=50)
    objeto=models.TextField(max_length=1200)
    numero=models.CharField(max_length=50,unique=True,blank=True)
    seguro = models.CharField(default=None, max_length=25, choices=(
        ('SIM', 'POSSUI SEGURO'),
        ('NÃO', 'NÃO POSSUI SEGURO'),
    ))
    tipo_documento=models.CharField(default='diversos', max_length=25, choices=(
        ('apolice', 'apolice de seguro'),
        ('seg.boleto', 'boleto de seguro'),
        ('contrato', 'contrato assinado'),
        ('diversos', 'documentos diversos'),
    ))
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.contrato_upload_path,
        validators=[validade_pdf],
        verbose_name="Documentos",

    )
    seguradora = models.CharField(max_length=100, blank=True, null=True, verbose_name="Seguradora")
    inicio=models.DateField()
    vigencia=models.CharField(max_length=50)
    fim_contrato=models.DateField()
    valor_total = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor Total")
    observacoes=models.TextField(max_length=1800)
    show=models.BooleanField(default=True)
'''


