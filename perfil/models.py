from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# from datetime import date
from django.forms import ValidationError
# Create your models here.
import re
from utils import tools_utils

class PerfilUsuario(models.Model):
    usuario=models.OneToOneField(User,max_length=50,on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100,null=True,blank=True )
    idade=models.IntegerField(validators=[
        MaxValueValidator(125),
        MinValueValidator(18)
    ],blank=True,)
    data_nascimento=models.DateField()
    endereco = models.CharField(max_length=250, null=True,blank=True)
    cpf=models.CharField(max_length=12,)
    setor = models.CharField(default=None, max_length=5, choices=(
        ('ADM', 'ADMINISTRAÇÃO'),
        ('COM', 'COMERCIAL'),
        ('PRD', 'PRODUÇÃO'),
        ('RH',  'RECURSOS HUMANOS'),
        ('FIN', 'FINANCEIRO'),
    ))
    cargo = models.CharField(max_length=100, )
    funcao = models.CharField(max_length=100, )

    tipo_documento = models.CharField(default='diversos', max_length=25, choices=(
        ('REGISTRO', 'DOCS ADMISSAO'),
        ('COMPROVANTES', 'COMPROVANTES'),
        ('REEMBOLSO', 'NOTAS DE REEMBOLSO'),
        (' SAUDE', 'DOCS MEDICOS'),
        ('ADVERTENCIAS', 'ADVS E MULTAS'),
        ('JUDICIAIS', 'DOCS JUDICIAIS'),

    ))
    documentos = models.FileField(
        blank=True,
        upload_to=tools_utils.docs_rh_load_path,
        verbose_name="Documentos ", max_length=255, null=True)
    ocorrencias = models.TextField(blank=True, max_length=5000, default='')



    def __str__(self):
        return self.usuario.username
        '''quando usar o one to one field lembrar de se usar User, 
        no self.xxxx do def str
        retornar o username'''

# para fazer validação de canpos, estudar a logica
    def clean(self):
        error_messages={}
        if not tools_utils.valida_cpf(self.cpf):
            error_messages['cpf']='Dgite um cpf valido'


        if error_messages:
            raise ValidationError(error_messages)



    class Meta:
        verbose_name='Colaborador'
        verbose_name_plural='Recursos Humanos'