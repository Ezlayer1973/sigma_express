import http
import sys, os, base64
from datetime import datetime
from fastapi import FastAPI, Response, status, Body, APIRouter, Depends,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from decouple import config

# Asegúrate de que backend esté en sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from conexion import DAO
from d_usuariosapp import *
from entidades import *

# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import *
from oauth2 import create_access_token # type: ignore
from oauth2 import get_current_user # type: ignore


# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')
#


dao=DAO()
connection = dao.connection

router = APIRouter(
    tags=['Autenticacion']
) 

@router.post("/login", response_model=e_token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()): #name function thats no matter        
    try:        
        v_parametros = [
            user_credentials.username,
            user_credentials.password
        ]
        print(v_parametros)
        c_usuarios = d_unusuarioapp(connection,v_parametros[0],)     
        print(c_usuarios)     
        if c_usuarios == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email no registrado")       
        else:          
            v_key = str_to_key(v_llave)                                    
            clave_almacenada=c_usuarios[-2]
            v_codigo=c_usuarios[-1]
            print(v_codigo)
            v_key = str_to_key(v_llave)        
            v_bd = desencripta(base64.urlsafe_b64decode(clave_almacenada),v_key)
            v_password = v_parametros[1]   
            v_email = c_usuarios[0]                           
        
            if v_bd != v_password:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password incorrecto")
            else:                
                v_token = create_access_token(data = {"email": v_email, "codigo": v_codigo})
                return {"access_token": v_token, "token_type": "bearer"}

    except HTTPException as e:
        # Devolver una respuesta adecuada en caso de error HTTP
        raise e    