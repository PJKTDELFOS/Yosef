
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
    nomecompleto=models.OneToOneField(User,max_length=50,on_delete=models.CASCADE)#transformar em charfiede
    data_nascimento=models.DateField()
    endereco = models.CharField(max_length=250, null=True,blank=True)
    n_residencial=models.CharField(max_length=250, null=True,blank=True)
    bairro=models.CharField(max_length=250, null=True,blank=True)
    cidade=models.CharField(max_length=250, null=True,blank=True)
    estado = models.CharField(default=None, max_length=2, choices=(
        ('AC', 'Acre'),('AL', 'Alagoas'),  ('AP', 'Amapá'),  ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'),('DF', 'Distrito Federal'),  ('ES', 'Espírito Santo'),  ('GO', 'Goiás'),
        ('MA', 'Maranhão'),  ('MT', 'Mato Grosso'),  ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),('TO', 'Tocantins'),
    ))
    complemento=models.CharField(max_length=250, null=True,blank=True)
    cep=models.CharField(max_length=9,)
    cpf=models.CharField(max_length=12,)
    rg=models.CharField(max_length=12,)
    setor = models.CharField(default=None, max_length=5, choices=(
        ('ADM', 'ADMINISTRAÇÃO'),('COM', 'COMERCIAL'),
        ('OPR', 'OPERACIONAL'),('RH',  'RECURSOS HUMANOS'),
        ('FIN', 'FINANCEIRO'),
    ))
    nacional=models.CharField(default=None, max_length=25, choices=(
        ('Nacional', 'Brasileiro'),
        ('Estrangeiro', 'Estrangeiro'),
    ))

    cargo = models.CharField(max_length=100, )
    tipo_documento = models.CharField(default='diversos', max_length=25, choices=(
        ('', ''), ('REGISTRO', 'DOCS ADMISSAO'),  ('COMPROVANTES', 'COMPROVANTES'),
        ('REEMBOLSO', 'NOTAS DE REEMBOLSO'),(' SAUDE', 'DOCS MEDICOS'),
        ('ADVERTENCIAS', 'ADVS E MULTAS'), ('JUDICIAIS', 'DOCS JUDICIAIS'),

    ),blank=True)
    documentos = models.FileField(
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
    banco=models.CharField(default=None, max_length=250, null=True,blank=True)
    agencia=models.CharField(default=None, max_length=250, null=True,blank=True)
    n_conta_banco=models.CharField(default=None, max_length=250, null=True,blank=True,verbose_name='Numero da conta')


    def idade(self):
        atual=datetime.now()
        idade=atual.year - self.data_nascimento.year
        return idade

    def __str__(self):
        return self.usuario.username


# para fazer validação de canpos, estudar a logica
    def clean(self):
        error_messages={}
        if not tools_utils.valida_cpf(self.cpf):
            error_messages['cpf']='Dgite um cpf valido'
        if error_messages:
            raise ValidationError(error_messages)
        if not re.search(r'[^0-9]',self.cep) or len(self.cep)<8:
            error_messages['cep'] = 'Dgite um cep valido'
    class Meta:
        verbose_name='Colaborador'
        verbose_name_plural='Recursos Humanos'


# class conjuge(models.Model):
#     pass
# class dependente(models.Model):
#     pass
#
# class beneficios(models.Model):
#     pass
# class uniformes(models.Model):
#     pass
'''
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

'''

'''
quando usar o one to one field 
lembrar de se usar User, 
no self.xxxx do def str
retornar o username
'''