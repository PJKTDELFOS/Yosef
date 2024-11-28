from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User  # para o user que vai cadastrar e operar o sistema
# Create your models here.
from utils import tools_utils





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
        return f' {self.modalidade} {self.contratante} {self.numero_licitacao} '

    def valor_formatado(self):
        return tools_utils.formata_preco(self.valor_total)
    valor_formatado.short_description='Valor'

class Contratos (models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, blank=False, null=False,related_name='contratos')
    contratante=models.CharField(max_length=50)
    objeto=models.TextField(max_length=1200)
    numero=models.CharField(max_length=50,unique=True,blank=True)
    seguro = models.CharField(default=None, max_length=25, choices=(
        ('SIM', 'POSSUI SEGURO'),
        ('NÃO', 'NÃO POSSUI SEGURO'),
    ))
    tipo_documento=models.CharField(default='diversos', max_length=25, choices=(
        ('', ''),
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
    apolice=models.CharField(default=None, max_length=100,)
    inicio=models.DateField()
    vigencia=models.CharField(max_length=50)
    fim_contrato=models.DateField()
    valor_total = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor Total")
    observacoes=models.TextField(max_length=1800)
    show=models.BooleanField(default=True)


    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"


    def __str__(self):
        return f'{self.contratante} {self.numero}'

#aaa
    def executado(self):
        pedidos = Pedidos.objects.filter(contrato=self)
        total_executado=sum(pedido.valor for pedido in pedidos)
        return total_executado

    def executavel(self):
        executavel= self.valor_total-self.executado()
        return executavel

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
    tipo_documento = models.CharField(default='diversos', max_length=25, choices=(
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


    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"




