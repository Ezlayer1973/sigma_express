# Creo entidades con datos default,inclusive pueden ser omitidos por el POST request
from ast import Num
import decimal
import string
from turtle import st
from typing import Optional
# from networkx import connected_watts_strogatz_graph
from pydantic import BaseModel,EmailStr, ConfigDict
from datetime import datetime
from decimal import Decimal

class e_usuario(BaseModel):    
    codigo: int
    apellynom: str
    clave: str
    cod_ofi: int = 1
    fecha_alta: str
    usuario: str
    baja: bool = False
    cod_sis4: int = 1
     
class e_usuarioresp(BaseModel):
    codigo: int
    fecha_actu: datetime

class e_usuarioapp(BaseModel):  
    email: EmailStr    
    password: str        
    apellido: str
    nombres: str
    direccion_fac: str
    localidad_fac: str
    cod_postal_fac: str
    provincia_fac: str
    telefono: str
    direccion_env: str
    localidad_env: str
    cod_postal_env: str
    provincia_env: str    
    fecha_alta: datetime            
    baja: bool = False      
    tipo_doc: str
    nro_doc: int
    
class e_usuarioappresp(BaseModel):    
    codigo: int
    fecha_alta: datetime

class e_token(BaseModel):
    access_token: str
    token_type: str

class e_tokendata(BaseModel):
    id: Optional[str] = None 
    codigo: int 
    
class e_pedidos(BaseModel):
    id: int
    cod_cli: int
    fecha: datetime
    hora: str
    nro_comp: int
    baja: bool = False
    letra: str
    sucursal: int
    cod_usuapp: int

class e_expedientes(BaseModel):
    fecha: datetime
    concepto: str
    iniciador: str
    doc_inic: int
    estado: str
    fecha_actu: datetime
    cod_ofiactual: int
    baja: bool = False
    codigo: int
    numero: int
        
class e_articuloapp(BaseModel):
    id: int   
    codigo: str
    cod_padre: int
    cod_rub: int
    descri: str
    precio_c: Decimal
    utilidad: Decimal
    precio_v: Decimal
    precio_iva: Decimal
    stock: Decimal
    fecha_actu: datetime
    porc_iva: Decimal
    cantxum: Decimal
    um: str
    libre: Decimal
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
      
         

      