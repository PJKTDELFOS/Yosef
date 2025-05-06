import unicodedata
from django.template import Library
from openpyxl import load_workbook
from django import template
import os
from django.conf import settings
import unidecode

register=Library()
@register.filter
def formata_preco(val):
    return f'R$:{val:.4f}'.replace('.',',')



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
    funcionario_arquivos = (f'{instance.cpf or "novo"}')
    tipo_documento = sanitize_name(instance.tipo_documento)

    return os.path.join(f'rh/{funcionario_arquivos}/{tipo_documento}', filename)


def docs_finan_load_path(instance,filename):
    vencimento = instance.vencimento
    subpasta=instance.pk
    arquivo=instance.documentos
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'financeiro/pagamento/{vencimento}/{subpasta}/',filename )

def docs_finan_load_path_rcbm(instance,filename):
    data_pgto = instance.data_pgto
    subpasta=instance.origem
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'financeiro/recebimento/{data_pgto}/{subpasta}/',filename )

def documentos_load_path(instance,filename):
    documento = instance.documento
    setor=instance.pedido_origem
    tipo=instance.tipo_documento
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'documentos/{setor}/{tipo}/{documento}/',filename )


def documentos_frota_load_path(instance,filename):
    placa=instance.placa
    ativo = instance.Ativo
    nome_ativo=f'{ativo}-{placa}'
    tipo_ativo=instance.tipo.tipo_de_ativo
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'operacional/frota/{tipo_ativo}/{nome_ativo}/',filename )

def documentos_manutencao_frota_load_path(instance,filename):
    placa=instance.Ativo_em_manutencao.placa
    ativo = instance.Ativo_em_manutencao.Ativo
    nome_ativo=f'{ativo}-{placa}'
    tipo_ativo=instance.Ativo_em_manutencao.tipo.tipo_de_ativo
    operacao=instance.operacao
    ordem=instance.pk
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'operacional/frota/{tipo_ativo}/{nome_ativo}/manutencao/{operacao}/Ordem nº{ordem}/',filename )

def documentos_amoxarifado_load_path(instance,filename):
    tipo=instance.item.tipo
    nome=instance.item.nome
    lote=instance.nota
    filename=unidecode.unidecode(filename.replace(" ", "_"))
    return os.path.join(f'operacional/almoxarifado/'
                        f'{tipo}/{nome}/lotes/{lote}/',filename )

# ser operacional/frota/ativo/tipo_ativo/nome_ativo/manutencao/tipo/ordem/filename
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



class CalculadoraCustoTotal:
    def __init__(self, instance):
        self.instance=instance

    def calcular_total_alocado(self):
        return sum(
            recurso_alocado.custo_total() for
            recurso_alocado in
            self.instance.recurso_alocados.all())




# def docs_finan_load_path(instance, filename):
#     funcionario_arquivos = (f'{instance.pk or "novo"}-{sanitize_name(instance.nome)}'
#                      f'-{sanitize_name(instance.cpf)}')
#     tipo_documento = sanitize_name(instance.tipo_documento)
#
#     return os.path.join(f'rh/{funcionario_arquivos}/{tipo_documento}', filename)


#fazer upload paths especificos e trocar o nome da pasta