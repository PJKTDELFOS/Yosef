
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# from datetime import date
from django.forms import ValidationError
# Create your models here.
import re
from datetime import datetime
from utils import tools_utils
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

class cadastrofuncionario(models.Model):
    nomecompleto=models.CharField(max_length=50,blank=False)#transformar em charfiede
    data_nascimento=models.DateField()
    endereco = models.CharField(max_length=250, null=True,blank=True)
    n_residencial=models.CharField(max_length=250, null=True,blank=True)
    bairro=models.CharField(max_length=250, null=True,blank=True)
    cidade=models.CharField(max_length=250, null=True,blank=True)
    UF = models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ))
    complemento=models.CharField(max_length=250, null=True,blank=True)
    cep=models.CharField(max_length=9,)
    documento = models.CharField(default='diversos', max_length=100, choices=(
        ('CNH', 'CNH'), ('CTPS', 'CARTEIRA DE TRABALHO'), ('RG', 'RG'),
        ('CPF', 'CPF'), (' TITULO-ELEITOR', 'TITULO ELEITOR'),
        ('CERTIFICADO RESERVISTA', 'CAM'), ('CERTIFICADOS', 'CERTIFICADOS'),

    ), blank=True, )
    cpf=models.CharField(max_length=12,)
    naturalidade=models.CharField(max_length=250,null=True,blank=True)
    rg=models.CharField(max_length=12,)
    orgao_expedidor_rg=models.CharField(max_length=12,)
    uf_rg=models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ))
    data_emissao_rg=models.DateField()
    n_titulo_eleitor=models.CharField(max_length=12,)
    zona_eleitor=models.CharField(max_length=12,)
    secao=models.CharField(max_length=12,)
    setor = models.CharField(default=None, max_length=5, choices=(
        ('ADM', 'ADMINISTRAÇÃO'),('COM', 'COMERCIAL'),
        ('OPR', 'OPERACIONAL'),('RH',  'RECURSOS HUMANOS'),
        ('FIN', 'FINANCEIRO'),
    ))
    n_cnh=models.CharField(max_length=50,)
    categoria_cnh=models.CharField(max_length=50,)
    vencimento_cnh=models.DateField()
    reservista=models.BooleanField(default=False,verbose_name='Reservista')
    n_cam=models.CharField(max_length=50,)

    nacional=models.CharField(default=None, max_length=25, choices=(
        ('Nacional', 'Brasileiro'),
        ('Estrangeiro', 'Estrangeiro'),
    ))
    cargo = models.CharField(max_length=100, )
    documento = models.CharField(default='diversos', max_length=100, choices=(
        ('', ''), ('CTPS', 'CARTEIRA DE TRABALHO'), ('RG', 'RG'),
        ('CPF', 'CPF'), (' TITULO-ELEITOR', 'TITULO ELEITOR'),
        ('CERTIFICADO RESERVISTA', 'CAM'), ('CERTIFICADOS', 'CERTIFICADOS'),
    ), blank=True, )
    tipo_documento = models.CharField(default='diversos', max_length=125, choices=(
        ('', ''), ('REGISTRO','REGISTRO'),('COMPROVANTES', 'COMPROVANTES'),
        ('REEMBOLSO', 'NOTAS DE REEMBOLSO'),(' SAUDE', 'DOCS MEDICOS'),
        ('ADVERTENCIAS', 'ADVS E MULTAS'), ('JUDICIAIS', 'DOCS JUDICIAIS'),
    ),blank=True,)
    arquivos = models.FileField(
        blank=True,
        upload_to=tools_utils.docs_rh_load_path,
        verbose_name="Documentos ", max_length=255, null=True)
    ocorrencias = models.TextField(blank=True, max_length=5000, default='')
    nome_mae=models.CharField(default=None, max_length=250, null=True,blank=True)
    nome_pais=models.CharField(default=None, max_length=250, null=True,blank=True)
    telefone=models.CharField(default=None, max_length=250, null=True,blank=True)
    celular=models.CharField(default=None, max_length=250, null=True,blank=True)
    email=models.EmailField(default=None, max_length=250, null=True,blank=True)
    estado_civil=models.CharField(default=None, max_length=250, null=True,choices=(
        ('solteiro(a)','solteiro(a)'), ('casado(a)','casado(a)'), ('divorciado(a)','divorciado(a)'),
        ('viuvo(a)','viuvo(a)'),('nao informado','nao informado'),
    ))
    formacao_academica=models.CharField(default=None, max_length=250, null=True,choices=(
        ('fundamental incompleto','fundamental inccompleto'),('fundamental completo','fundamental completo'),
        ('Ensino Medio incompleto','Ensino Medio inccompleto'), ('Ensino medio Completo','Ensino medio Completo'),
        ('Gradução superior incompleta','Graduação superior inccompleto'), ('Bacharelado','Bacharelado'),
        ('Pos/especialização', 'pos/especialização'),
    ))
    curso_superior=models.CharField(default=None, max_length=250, null=True,blank=True)
    pos_especializacao=models.CharField(default=None, max_length=250, null=True,blank=True)#somente se  formaçao corresponder
    ctps=models.CharField(default=None, max_length=250, null=True,blank=True)
    serie=models.CharField(default=None, max_length=250, null=True,blank=True)

    uf_emissao_ctps=models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ))
    pis=models.CharField(default=None, max_length=250, null=True,blank=True)
    banco=models.CharField(default=None, max_length=250, null=True,blank=True)
    agencia=models.CharField(default=None, max_length=250, null=True,blank=True)
    n_conta_banco=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Numero da conta')
    salario=models.DecimalField(default=0.00, null=True,blank=True,decimal_places=2,max_digits=10)
    nome_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    cpf_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    rg_conjuge=models.CharField(default=None, max_length=250, null=True,blank=True)
    data_nascimento_conjuge = models.DateField()

    vale_transporte=models.DecimalField(default=0.00, null=True,blank=True,decimal_places=2,max_digits=10)
    vale_alimentacao=models.DecimalField(default=0.00, null=True,blank=True,decimal_places=2,max_digits=10)
    usuario=models.OneToOneField(User,on_delete=models.CASCADE,related_name='perfil',blank=True,null=True,default=None)

    def idade(self):
        atual=datetime.now()
        idade=atual.year - self.data_nascimento.year
        return idade

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





class uniformes_EPI(models.Model):

    class Meta:
        verbose_name='Uniforme'
        verbose_name_plural='Uniformes'

    funcionario=models.OneToOneField(cadastrofuncionario,on_delete=models.CASCADE)
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
    funcionario = models.OneToOneField(cadastrofuncionario, on_delete=models.CASCADE)
    nome_dependente = models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Nome dependente')
    cpf_dependente=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='CPF_dependente')
    grau_relacional=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Grau relacional',
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
'''