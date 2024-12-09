from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User  # para o user que vai cadastrar e operar o sistema
import pytz
from utils import tools_utils
from datetime import datetime
from openpyxl import load_workbook
import os
from django.conf import settings
# Create your models here
def validade_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('somente arquivos PDF')



class Processo(models.Model):
    numero_processo=models.CharField(max_length=50,blank=False,verbose_name='Processo ADM')
    numero_licitacao=models.CharField(max_length=50,blank=False,verbose_name='Licitação nª')
    contratante=models.CharField(max_length=50,blank=True,)
    modalidade=models.CharField( max_length=25, choices=(
        ('PE', 'PREGAO ELETRONICO'),
        ('PP', 'PREGÃO PRESENCIAL'),
        ('CC', 'CONCORRENCIA'),
        ('TP', 'TOMADA DE PREÇOS'),
        ('LE', 'LEILÃO'),
        ('DL', 'DISPENSA'),
        ('CD', 'COMPRA DIRETA'),
        ('COT','COTAÇÃO'),
    ),blank=False)
    data_disputa=models.DateTimeField(blank=False,default=timezone.now)
    objeto=models.TextField(max_length=500,blank=False,verbose_name='Objeto')
    tipo = models.CharField( max_length=25, choices=(
        ('GLOBAL', 'PREÇO GLOBAL'),
        ('LOTE', 'PREÇO POR LOTE'),
        ('ITEM', 'PREÇO POR ITEM'),
        ('MAIOR OFERTA', 'LEILAO E OU CESSÃO'),
    ),blank=False)
    valor_total=models.DecimalField(max_digits=18, decimal_places=2,default=0.00,null=True,blank=True)
    status = models.CharField( max_length=25, choices=(
        ('CADASTRAR', 'CADASTRAR PROPOSTA'),
        ('CADASTRADO', 'PROPOSTA CADASTRADA'),
        ('ACOMPANHAR', 'EM ACOMPANHAMENTO'),
        ('RECURSO', 'FAZER RECURSO'),
        ('CONTRA-RAZÃO', 'FAZER CONTRA RAZAO'),
        ('HOMOLOGADO', 'HOMOLAGADO'),
        ('ASSINADO', 'CONTRATO ASSINADO'),
    ),blank=False)
    ocorrencias=models.TextField(max_length=500,blank=True,)
    tipo_documento = models.CharField(default=None, max_length=25, choices=(
        ('', ''),
        ('EDITAL', 'EDITAL E ANEXOS'),
        ('BOOK', 'BOOK USADO'),
        ('PEÇAS JURIDICCAS', 'PEÇAS JURIDICAS'),
        ('DIVERSOS', 'DOCUMENTOS DIVERSOS'),
    ),blank=True)
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.processo_upload_path,
        verbose_name='arquivo',)
    show = models.BooleanField(default=True)


    def __str__(self):
        return f' {self.modalidade} {self.contratante} {self.numero_processo} '

    def valor_formatado(self):
        return tools_utils.formata_preco(self.valor_total)
    valor_formatado.short_description='Valor'

    # def save(self, *args, **kwargs):
    #     #is_new=self.pk is None
    #     # aqui salva e cria o pk antes de salvar o
    #     # arquivo, vou ter de adaptar ja no template ,
    #     # forms e  viewsa antes de testar
    #     super().save(*args, **kwargs)


class Contratos (models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='contratos')
    contratante=models.CharField(max_length=50,blank=False,null=False,verbose_name='Contratante')
    objeto=models.TextField(max_length=1200,blank=False,verbose_name='Objeto',null=False)
    numero=models.CharField(max_length=50,blank=False,null=False,default='')
    seguro = models.CharField(default='',blank=True, max_length=25,null=False, choices=(
        ('', ''),
        ('SIM', 'POSSUI SEGURO'),
        ('NÃO', 'NÃO POSSUI SEGURO'),
    ))
    tipo_documento=models.CharField(default='', max_length=25,blank=True,null=False, choices=(
        ('', ''),
        ('apolice', 'apolice de seguro'),
        ('seg.boleto', 'boleto de seguro'),
        ('contrato', 'contrato assinado'),
        ('diversos', 'documentos diversos'),
    ))
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.contrato_upload_path,
        verbose_name="Documentos",

    )
    seguradora = models.CharField(max_length=100, blank=True, null=False, verbose_name="Seguradora")
    apolice=models.CharField(max_length=100,blank=False,null=False,)
    inicio=models.DateField(blank=True,null=False,default=timezone.now)
    vigencia=models.CharField(max_length=50,blank=True,null=False,default='')
    fim_contrato=models.DateField(blank=True,null=False,default=timezone.now)
    valor_total = models.DecimalField(max_digits=18,blank=False, decimal_places=2,null=False,default=0.00,
                                      verbose_name="Valor Total")
    observacoes=models.TextField(max_length=1800,blank=False,null=False,default='')
    show=models.BooleanField(default=True,blank=False,)


    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"


    def __str__(self):
        return f'{self.numero}'

#aaa
    def executado(self):
        pedidos = Pedidos.objects.filter(contrato=self)
        total_executado=sum(pedido.valor for pedido in pedidos)
        return total_executado

    def executavel(self):
        executavel= self.valor_total-self.executado()
        return executavel

    # def save(self, *args, **kwargs):
    #     #is_new=self.pk is None
    #     # aqui salva e cria o pk antes de salvar o
    #     # arquivo, vou ter de adaptar ja no template ,
    #     # forms e  viewsa antes de testar
    #     super().save(*args, **kwargs)

class Pedidos(models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE, related_name='pedidos')
    numero=models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_origem=models.DateField(blank=True,null=True)
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
    tipo_documento = models.CharField(default='', max_length=25, choices=(
        ('', ''),
        ('RELATORIOS', 'RELATORIOS'),
        ('PEDIDO', 'PEDIDO'),
        ('NOTAS REEMBOLSO', 'NOTAS DE REEMBOLSO'),
        ('NF PARA FATURA', 'NOTAS DE FATURAMENTO'),
        ('ACEITE', 'ACEITES'),
        ('DIVERSOS', 'ACEITES'),

    ),blank=True)
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.pedido_upload_path,
        verbose_name="Documentos ", max_length=255,)
    endereco_entrega=models.TextField(blank=True,default='',max_length=1800)
    observacoes=models.TextField(blank=True,default='',max_length=1800)
    data_hora_att=models.DateTimeField(blank=True,null=True,auto_now=True,)



    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f' Pedido nº {self.numero}, Contrato {self.contrato}'

    def criar_planilha(self):
        template_form = os.path.join(settings.BASE_DIR, 'processos/templates/planilhas/modelo_pedido.xlsx')
        name = f'Pedido-{str(self.numero)}-{str(self.contratante)}'
        save_path = tools_utils.pedido_upload_path(self, f'{name}.xlsx')
        if os.path.exists(save_path):
            print(f"Atualizando planilha existente em: {save_path}")
            print(save_path, 'atualizando a planilha ')
        else:
            try:
                workbook = load_workbook(filename=template_form)
                worksheet = workbook['sheet']

                br_tz=pytz.timezone('America/Sao_Paulo')

                data_origem = str(self.data_origem) if self.data_origem else ''
                data_entrega = str(self.data_entrega) if self.data_entrega else ''
                data_hora_att=self.data_hora_att.astimezone(br_tz).strftime('%d/%m/%Y %H:%M:%S') if self.data_hora_att else ''
                recebimento_empenho=str(self.recebimento_empenho) if self.recebimento_empenho else ''
                worksheet['I9'] = self.numero
                worksheet['I10'] = data_origem #criação
                worksheet['I12'] = self.cnpj_contratante
                worksheet['B12'] = self.contratante
                worksheet['A15'] = str(self.contrato)
                worksheet['C15'] = self.empenho
                worksheet['D15'] = self.ordem_fornecimento
                worksheet['E15'] = recebimento_empenho # recebimento empenho
                worksheet['G15'] = self.contato
                worksheet['H15'] = self.telefone
                worksheet['I15'] = self.email
                worksheet['D17'] = self.objeto
                worksheet['B16'] = data_entrega
                worksheet['D16'] = self.endereco_entrega
                worksheet['A21'] = self.unidade_fornecimento
                worksheet['B21'] = self.qtde
                worksheet['A23'] = self.observacoes
                worksheet['B51'] = self.coordenador
                worksheet['I11'] = data_hora_att    #ultima modifica
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                workbook.save(filename=save_path)
                print(save_path,'caminho da planilha do models ')
                print(f'planilha salva como {name}.xlsx')
            except Exception as e:
                name = f'Pedido_nº{self.numero}_contrato:{self.contrato}'
                print(f"Erro na planilha: {e}, pedido {name} nao  se nao puder fazer a planilha ")


    def save(self, *args, **kwargs):
        #is_new=self.pk is None
        # aqui salva e cria o pk antes de salvar o
        # arquivo, vou ter de adaptar ja no template ,
        # forms e  viewsa antes de testar
        super().save(*args, **kwargs)
        self.criar_planilha()







