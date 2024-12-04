from django.template import Library
from openpyxl import load_workbook
from django import template
import os
from django.conf import settings

register=Library()
@register.filter
def formata_preco(val):
    return f'R$:{val:.2f}'.replace('.',',')



import re

def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]                 # Elimina os dois últimos digitos do CPF
    reverso = 10                        # Contador reverso
    total = 0

    # Loop do CPF
    for index in range(19):
        if index > 8:                   # Primeiro índice vai de 0 a 9,
            index -= 9                  # São os 9 primeiros digitos do CPF

        total += int(novo_cpf[index]) * reverso  # Valor total da multiplicação

        reverso -= 1                    # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:                   # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0                   # Zera o total
            novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False



import os

def sanitize_name(value):
    """Remove caracteres especiais e substitui espaços por underscores."""
    return ''.join(e if e.isalnum() or e == '_' else '_' for e in value.replace(' ', '_'))

def processo_upload_path(instance, filename):
    processo_nome = (f'{instance.pk or "novo"}')

    tipo_documento = sanitize_name(instance.tipo_documento)

    return os.path.join(f'processos/{processo_nome}/{tipo_documento}', filename)

def contrato_upload_path(instance, filename):
    processo_nome = (f'{instance.processo.pk or "novo"}')
    contrato_nome = (f'{instance.pk or "novo"}')
    tipo_documento = sanitize_name(instance.tipo_documento)

    return os.path.join(f'processos/{processo_nome}/contratos/{contrato_nome}/{tipo_documento}', filename)

def pedido_upload_path(instance, filename):
    processo_nome = (f'{instance.contrato.processo.pk or "novo"}')

    contrato_nome = (f'{instance.contrato.pk or "novo"}')

    pedido_nome = (f'{instance.pk or "novo"}')

    tipo_documento = sanitize_name(instance.tipo_documento)

    return os.path.join(
        settings.MEDIA_ROOT,'processos',processo_nome,'contratos',
        contrato_nome,'pedidos',pedido_nome,tipo_documento,filename
    )

# settings.MEDIA_ROOT, 'processos', processo_nome, 'contratos', contrato_nome, 'pedidos', pedido_nome, tipo_documento, filename

def docs_rh_load_path(instance, filename):
    funcionario_arquivos = (f'{instance.pk or "novo"}')
    tipo_documento = sanitize_name(instance.tipo_documento)

    return os.path.join(f'rh/{funcionario_arquivos}/{tipo_documento}', filename)






def criar_pedido(instance,filename):
    template_form = 'modelo_pedido.xlsx'
    workbook = load_workbook(filename=template_form)
    worksheet = workbook['sheet']
    worksheet['I9'] = instance.numero
    worksheet['I10'] = instance.data_origem
    worksheet['I12'] = instance.cnpj_contratante
    worksheet['B12'] = instance.contratante
    worksheet['A15'] = instance.contrato
    worksheet['C15'] = instance.empenho
    worksheet['D15'] = instance.ordem_fornecimento
    worksheet['E15'] = instance.data_origem
    worksheet['G15'] = instance.contato
    worksheet['H15'] = instance.telefone
    worksheet['I15'] = instance.email
    worksheet['D17'] = instance.objeto
    worksheet['B16'] = instance.data_entrega
    worksheet['D16'] = instance.local_entrega
    worksheet['A21'] = instance.unidade_fornecimento
    worksheet['B21'] = instance.qtde
    worksheet['A23'] = instance.observacoes
    worksheet['B51'] = instance.coordenador
    name=f'Pedido nº{instance.numero}-contrato:{instance.contrato} contratante:{instance.contratante}'
    save_path=pedido_upload_path(instance,f'{name}.xlsx')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    workbook.save(filename=save_path)
    print(f"Planilha salva como '{name}.xlsx'.")




# def docs_finan_load_path(instance, filename):
#     funcionario_arquivos = (f'{instance.pk or "novo"}-{sanitize_name(instance.nome)}'
#                      f'-{sanitize_name(instance.cpf)}')
#     tipo_documento = sanitize_name(instance.tipo_documento)
#
#     return os.path.join(f'rh/{funcionario_arquivos}/{tipo_documento}', filename)


#fazer upload paths especificos e trocar o nome da pasta