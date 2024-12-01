from django import forms
from processos import models
from django.utils.timezone import localtime

class ProcessForm(forms.ModelForm):
    class Meta:
        model=models.Processo
        fields='__all__'
        exclude=['show']
        labels={
            'numero_processo':'Numero de Processo',
            'numero_licitacao':'Numero da licitação',
            'contratante':'Contratante',
            'modalidade': 'Modalidade',
            'data_disputa': 'Data disputa',
            'objeto': 'Objeto',
            'valor_total': 'Valor Total',
            'status': 'Status',
            'ocorrencias': 'Ocorrencias',
            'tipo_documento': 'Tipo Documento',
            'documentos': 'Inserir Documentos',
            'tipo': 'Tipo de Licitação',

        }
# aqui so vale impot para  date time
        #TEM QUE SER O EQUIVALENTE NO MODELS PARA DATEFIELD
        widgets={
            'data_disputa':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),#segurar data
            'objeto':forms.Textarea(attrs={'rows':4}),
            'ocorrencias': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva as ocorrências...'}),
            'status': forms.Select(),
            'tipo_documento': forms.Select(),
        }
        # segurar a data para atualização ja que e o mesmo form para ambos


        ''' forma de validaçao nos forms '''

    def clean(self):
        cleaned_data = super().clean()
        numero_processo = cleaned_data['numero_processo']
        numero_licitacao = cleaned_data['numero_licitacao']
        contratante = cleaned_data['contratante']
        modalidade = cleaned_data['modalidade']
        data_disputa = cleaned_data['data_disputa']
        valor_total = cleaned_data['valor_total']

        if not numero_processo:
            print('falhou no numero processo')
            raise forms.ValidationError("este campo e obrigatorio 1")
        if not numero_licitacao:
            print('falhou no numero licitacao')
            raise forms.ValidationError("este campo e obrigatorio 2")
        if not contratante:
            print('falhou no contratante')
            raise forms.ValidationError("este campo e obrigatorio 3")
        if not modalidade:
            print('falhou no modalidade')
            raise forms.ValidationError("este campo e obrigatorio 4")
        if not data_disputa:
            print('falhou no data disputa')
            raise forms.ValidationError("este campo e obrigatorio 5")
        if not valor_total:
            print('falhou valor_total')
            raise forms.ValidationError("este campo e obrigatorio 6")
        if numero_processo and numero_licitacao and contratante and modalidade and data_disputa and valor_total:
            return cleaned_data
# quando for necessario  que um campo especifico assuma um valor,faça pela forms, ate ter coisa melhor
    #se nao por nenhum tipo, ele entra automatico em  diversos, e uma solução interessante, ate
    def clean_tipo_documento(self):
        tipo_documento = self.cleaned_data['tipo_documento']
        if not tipo_documento or tipo_documento == '':
            return 'DIVERSOS'
        return tipo_documento

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance and self.instance.data_disputa:
            self.fields['data_disputa'].initial = localtime(self.instance.data_disputa).strftime('%Y-%m-%dT%H:%M')
















