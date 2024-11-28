from time import localtime

from django import forms
from processos import models
from processos.models import Processo

class ContractForm(forms.ModelForm):
    class Meta:
        model=models.Contratos
        fields='__all__'
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

        }
        widgets={
            'inicio':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),
            'fim_contrato':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),
            'objeto':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder': 'Descreva as ocorrências...'},
                                    ),
            'seguro':forms.Select(),
            'tipo_documento':forms.Select(),
            'observacoes':forms.Textarea(attrs={'type':'textarea',
                                           'rows':5,
                                           'placeholder':'Observações...'},),

            'processo':forms.TextInput(attrs={'readonly':'readonly',})
            }

    def clean(self):
        cleaned_data = super().clean()
        contratante = cleaned_data.get('contratante')
        objeto = cleaned_data.get('objeto')
        numero = cleaned_data.get('numero')
        seguradora = cleaned_data.get('seguradora')
        seguro = cleaned_data.get('seguro')
        tipo_documento = cleaned_data.get('tipo_documento')
        documento = cleaned_data.get('documento')

        if not contratante:
            print('falhou no CONTRATANTE')
            raise forms.ValidationError("este campo e obrigatorio 1")
        if not numero:
            print('falhou no numero')
            raise forms.ValidationError("este campo e obrigatorio 2")
        if not objeto:
            print('falhou no objeto')
            raise forms.ValidationError("este campo e obrigatorio 3")
        # se houver seguro ou seja  opção possui seguro, por a seguradora e apolice  é obrigatorio
        # if seguro and not seguradora:
        #     print('falhou na seguradora')
        #     raise forms.ValidationError("este campo e obrigatorio 4")
        # if (seguro and seguradora) and not tipo_documento:
        #     print('falhou na seguradora tipo')
        #     raise forms.ValidationError("Insira apolice e o boleto")
        # if (seguro and seguradora) and not documento:
        #     print('falhou na seguradora')
        #     raise forms.ValidationError("Insira apolice e o boleto")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processo'].required=False

        if  self.instance and self.instance.inicio:
            self.fields['inicio'].initial = localtime(self.instance.inicio).strftime('%Y-%m-%dT%H:%M')
        if  self.instance and self.instance.inicio:
            self.fields['fim_contrato'].initial=localtime(self.instance.inicio).strftime('%Y-%m-%dT%H:%M')
        if self.instance and self.instance.processo:
            self.fields['processo'].initial=self.instance.processo.numero_processo

    def clean_tipo_documento(self):
        tipo_documento = self.cleaned_data['tipo_documento']
        if not tipo_documento or tipo_documento == '':
            return ''
        return tipo_documento

'''
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
            
            seguro=self.cleaned_data['seguro']
            tipo_documento=self.cleaned_data['tipo_documento']
            
             apolicie = cleaned_data.get('apolicie')
        inicio = cleaned_data.get('inicio')
        vigencia = cleaned_data.get('vigencia')
        observacoes = cleaned_data.get('observacoes')


'''
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


