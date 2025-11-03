from core.entities.almoxarifado import (
TipoAtivoEntity,
Item_almoxarifadoEntity,
LoteEntity,
Item_alocadoEntity
)
from core.ports.almoxarifado_repository import AlmoxarifadoRepository

from operacional.models import (
lote as lote_model,
Item_almoxarifado as Item_Almoxarifado_Model,
Manutencao as Manutencao_Model,
Frota as Frota_Model,
tipo_ativo as tipo_ativo_model,
)
from core.entities.frota_e_equipamentos import frota_e_Equipamentos_Entity,Manutencao_entity
from core.ports.frota_repository import Frota_repository
from decimal import Decimal
from typing import List, Optional
from django.db.models import Sum


