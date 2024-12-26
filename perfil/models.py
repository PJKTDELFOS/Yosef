
from django.contrib.auth.models import User
import re
from django.db import models
from django.contrib.auth.models import User  # para o user que vai cadastrar e operar o sistema
from django.forms import ValidationError
from datetime import datetime
from utils import tools_utils
# Create your models here.


class cadastrofuncionario(models.Model):
    nomecompleto=models.CharField(max_length=50,blank=False,verbose_name='Nome completo')#transformar em charfiede
    data_nascimento=models.DateField()
    endereco = models.CharField(max_length=250, null=True,blank=True,verbose_name='endereço')
    n_residencial=models.CharField(max_length=250, null=True,blank=True,verbose_name='numero residencial')
    bairro=models.CharField(max_length=250, null=True,blank=True,verbose_name='bairro')
    cidade=models.CharField(max_length=250, null=True,blank=True,verbose_name='cidade')
    UF = models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ),verbose_name='Estado')
    complemento=models.CharField(max_length=250, null=True,blank=True,verbose_name='complemento')
    cep=models.CharField(max_length=9,verbose_name='cep',null=True,blank=True)
    cpf=models.CharField(max_length=12,verbose_name='cpf',null=True,blank=True)
    naturalidade=models.CharField(max_length=250,null=True,blank=True,verbose_name='naturalidade')
    rg=models.CharField(max_length=12,verbose_name='rg',null=True,blank=True)
    orgao_expedidor_rg=models.CharField(max_length=12,verbose_name='orgao expedidor rg',null=True,blank=True)
    data_emissao_rg=models.DateField(verbose_name='data emissao rg',)
    n_titulo_eleitor=models.CharField(max_length=12,verbose_name='Titulo de eleitor')
    setor = models.CharField(default=None, max_length=5, choices=(
        ('ADM', 'ADMINISTRAÇÃO'),('COM', 'COMERCIAL'),
        ('OPR', 'OPERACIONAL'),('RH',  'RECURSOS HUMANOS'),
        ('FIN', 'FINANCEIRO'),
    ),verbose_name='Setor')
    cargo = models.CharField(max_length=100, verbose_name='cargo')
    n_cnh=models.CharField(max_length=50,verbose_name='numero CNH')
    categoria_cnh=models.CharField(max_length=50,verbose_name='categoria CNH',)
    vencimento_cnh=models.DateField(verbose_name='vencimento CNH',)
    tipo_documento = models.CharField(default='diversos', max_length=125, choices=(
        ('', ''), ('REGISTRO','REGISTRO'),('COMPROVANTES', 'COMPROVANTES'),
        ('REEMBOLSO', 'NOTAS DE REEMBOLSO'),(' SAUDE', 'DOCS MEDICOS'),
        ('ADVERTENCIAS', 'ADVS E MULTAS'), ('JUDICIAIS', 'DOCS JUDICIAIS'),('CERTIFICADOS', 'CERTIFICADOS'),
        ('Documentos dependente', 'Documentos dependente'),
    ),blank=True,verbose_name='Tipo de documento')
    arquivos = models.FileField(
        blank=True,
        upload_to=tools_utils.docs_rh_load_path,
        verbose_name="Documentos ", max_length=255, null=True,)
    ocorrencias = models.TextField(blank=True, max_length=5000, default='',verbose_name='ocorrencias')
    nome_mae=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Nome da mãe')
    nome_pais=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Nome do pai')
    telefone=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Telefone')
    celular=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Celular')
    email=models.EmailField(default=None, max_length=250, null=True,blank=True,verbose_name='Email')
    sexo=models.CharField(default=None, max_length=250, null=True,blank=True,choices=(
        ('masculino','masculino'),('feminino','feminino'),('Nao Binario(a)(e)','Nao Binario(a)(e)'),
        ('Nao identificar', 'Nao Identificar'),
    ),verbose_name='Sexo')
    nacionalidade=models.CharField(default=None, max_length=250, null=True,blank=True,choices=(
        ('Brasileiro','Brasileiro'),('Estrangeiro','Estrangeiro'),
    ),verbose_name='nacionalidade')
    estado_civil=models.CharField(default=None, max_length=250, null=True,choices=(
        ('solteiro(a)','solteiro(a)'), ('casado(a)','casado(a)'), ('divorciado(a)','divorciado(a)'),
        ('viuvo(a)','viuvo(a)'),('nao informado','nao informado'),
    ),verbose_name='estado civil')
    formacao_academica=models.CharField(default=None, max_length=250, null=True,choices=(
        ('fundamental incompleto','fundamental inccompleto'),('fundamental completo','fundamental completo'),
        ('Ensino Medio incompleto','Ensino Medio inccompleto'), ('Ensino medio Completo','Ensino medio Completo'),
        ('Gradução superior incompleta','Graduação superior inccompleto'), ('Bacharelado','Bacharelado'),
        ('Pos/especialização', 'pos/especialização'),
    ),verbose_name='Escolaridade')
    curso_formacao=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Formaçao')
    ctps=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='CTPS')
    serie=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Serie')
    pis=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Pis')
    banco=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Banco')
    agencia=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Agencia')
    n_conta_banco=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Numero da conta')
    salario=models.DecimalField(default=0.00, null=True,blank=True,decimal_places=2,
                                max_digits=10,verbose_name='Salario')
    vale_transporte=models.DecimalField(default=0.00, null=True,blank=True,
                                        decimal_places=2,max_digits=10,verbose_name='Vale transporte')
    modal_transporte = models.TextField(blank=True, max_length=5000, default='',verbose_name='Modalidade de transporte')
    vale_alimentacao=models.DecimalField(default=0.00, null=True,blank=True,
                                         decimal_places=2,max_digits=10,verbose_name='Vale Alimentação')

    def idade(self):
        atual=datetime.now()
        idade=atual.year - self.data_nascimento.year
        return f'{idade} anos'

    def __str__(self):
        return f'funcionario CPF {self.cpf} nome completo {self.nomecompleto}'


# para fazer validação de canpos, estudar a logica
    def clean(self):
        error_messages={}

        salario=self.salario
        if salario < 0:
            error_messages['salario'] = 'salario errado'
        cpf_cadastrado=self.cpf or None
        cpf_db=None
        perfil=cadastrofuncionario.objects.filter(cpf=cpf_cadastrado).first()

        if perfil:
            cpf_db=perfil.cpf
            if cpf_db is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF ja existente'

        if not tools_utils.valida_cpf(self.cpf):
            error_messages['cpf']='Dgite um cpf valido'
        if error_messages:
            raise ValidationError(error_messages)
        if not re.search(r'[^0-9]',self.cep) or len(self.cep)<8:
            error_messages['cep'] = 'Dgite um cep valido'

    class Meta:
        verbose_name='Colaborador'
        verbose_name_plural='Recursos Humanos'


class Usuario_sistema(models.Model):
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
    funcionario=models.OneToOneField(cadastrofuncionario,on_delete=models.CASCADE,
                                     related_name='colaborador',verbose_name='Funcionario')
    usuario=models.OneToOneField(User,on_delete=models.CASCADE,related_name='usuario',verbose_name='Usuario')

    def __str__(self):
        return f'{self.funcionario.nomecompleto}-{self.usuario.username}'


class uniformes_EPI(models.Model):
    class Meta:
        verbose_name='Uniforme'
        verbose_name_plural='Uniformes'

    funcionario=models.ForeignKey(cadastrofuncionario,on_delete=models.CASCADE,related_name='uniforme_epi')
    tipo=models.CharField(default=None, max_length=250, null=True,blank=True,choices=(
        ('uniforme','uniforme'),
        ('EPI','EPI')
    ))
    acessorios=models.TextField(default=None, max_length=1500, null=True,blank=True,verbose_name='Acessorios')
    peca_superior=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Peca superior')
    tamanho_pecasuperior = models.CharField(default=None, max_length=250, null=True, blank=True,
                                            verbose_name='Tamanho peça superior', choices=(
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('EXG', 'EXG'),
    ))
    peca_inferior=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Peca inferior')
    tamanho_pecasupinferior = models.CharField(default=None, max_length=250, null=True, blank=True,
                                            verbose_name='Tamanho peça inferior', choices=(
            ('P', 'P'),
            ('M', 'M'),
            ('G', 'G'),
            ('GG', 'GG'),
            ('EXG', 'EXG'),
        ))
    sapatos=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Sapatos')
    tamanho_sapatos=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Tamanho')
    data_entrega=models.DateField()
    data_troca=models.DateField()
    motivo_troca=models.TextField(default=None, null=True, blank=True,verbose_name='Motivo troca',max_length=1500)


class dependente(models.Model):
    funcionario = models.ForeignKey(cadastrofuncionario, on_delete=models.CASCADE,related_name='dependente')
    nome_dependente = models.CharField(default=None, max_length=250, null=True,blank=False,verbose_name='Nome dependente')
    cpf_dependente=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='CPF_dependente')
    grau_relacional=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Relação',
                                     choices=(
                                         ('filho', 'filho'),
                                         ('genitor', 'genitor'),
                                         ('conjuge','conjuge'),
                                         ('avos', 'avos'),
                                         ('bisavos', 'bisavos'),
                                     ))

'''
quando usar o one to one field 
lembrar de se usar User, 
no self.xxxx do def str
retornar o username
from utils import tools_utils
from datetime import datetime
from openpyxl import load_workbook
import os
from django.conf import settings
import pytz
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
documento = models.CharField(default='diversos', max_length=100, choices=(
        ('CNH', 'CNH'), ('CTPS', 'CARTEIRA DE TRABALHO'), ('RG', 'RG'),
        ('CPF', 'CPF'), (' TITULO-ELEITOR', 'TITULO ELEITOR'),
        ('CERTIFICADO RESERVISTA', 'CAM'), 

    ), blank=True, )
    
    uf_emissao_ctps=models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ))
    
    documento = models.CharField(default='diversos', max_length=100, choices=(
        ('', ''), ('CTPS', 'CARTEIRA DE TRABALHO'), ('RG', 'RG'),
        ('CPF', 'CPF'), (' TITULO-ELEITOR', 'TITULO ELEITOR'),
        ('CERTIFICADO RESERVISTA', 'CAM'), ('CERTIFICADOS', 'CERTIFICADOS'),
    ), blank=True, )
    
     nome_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    cpf_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    rg_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    data_nascimento_conjuge = models.DateField()

'''