from django import forms
from financeiro.models import Centro_de_custo,Contas_a_pagar,Contas_a_receber

class Centro_de_custo_form(forms.ModelForm):
    class Meta:
        model=Centro_de_custo
        fields='__all__'



class Contas_a_pagar_form(forms.ModelForm):
    class Meta:
        model=Contas_a_pagar
        fields='__all__'
        widgets = {
            'vencimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_de_criacao': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }

class Contas_a_receber_form(forms.ModelForm):
    class Meta:
        model=Contas_a_receber
        fields='__all__'


'''
1-definir o contas a receber como acessar os pedidos, se vou por um botao no pedido ou 
vou por o botal no financeiro

2-definir os widegets do contas a pagar

3-definir os widegets do contas a receber
'''