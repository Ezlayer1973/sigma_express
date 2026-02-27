import sys, os, base64
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from decouple import config
import bcrypt  # agregá este import arriba

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from conexion import DAO
from d_usuarios import d_unusuario_login
from oauth2 import create_access_token

libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import *

v_llave = config('PO_')

dao = DAO()
connection = dao.connection

router = APIRouter(tags=['Autenticación'])

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        c_usuario = d_unusuario_login(connection, user_credentials.username)

        if c_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario no registrado"
            )

        # c_usuario = (codigo, apellynom, clave, usuario)
        v_key = str_to_key(v_llave)
        clave_almacenada = c_usuario[2]       

        if not bcrypt.checkpw(user_credentials.password.encode(), clave_almacenada.encode()):
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contraseña incorrecta"
            )
        
        v_token = create_access_token(data={
            "codigo": c_usuario[0],
            "usuario": c_usuario[3],
            "apellynom": c_usuario[1]
        })
        return {"access_token": v_token, "token_type": "bearer"}

    except HTTPException as e:
        raise e
    except Exception as ex:
        print("Error en login", ex)
        raise HTTPException(status_code=500, detail="Error interno")