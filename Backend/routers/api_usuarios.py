import sys, os,json
from datetime import datetime
from fastapi import FastAPI, Response, status, Body, APIRouter
from decouple import config

# Asegúrate de que backend esté en sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from conexion import DAO
from d_usuarios import *
from entidades import *

# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import * # type: ignore

# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')
#

dao=DAO()
connection = dao.connection


router = APIRouter(
    prefix="/users",
    tags=['Usuarios ERP']
) 

@router.get("/")
async def users():              #name function has no matter
    try:
        c_usuarios = d_listarusuarios(connection)
        converted_data = []
        for record in c_usuarios:
            usuario_data = e_usuario(
                codigo=record[0],
                apellynom=record[1],
                clave=record[2],
                cod_ofi=record[3],
                fecha_alta=dtoc(record[4]),
                usuario=record[5],
                baja=record[6],
                cod_sis4=record[7]
            )
            converted_data.append(usuario_data.model_dump())
        
        print(converted_data)                    
        return converted_data
    except Exception as ex:
        print("Error al consultar usuarios", ex)

# un usuario
@router.get("/{v_id}")    #cuando uso parametros por path debo tener cuidado. si creo una subpagina /userpath/ultimo por ej, ultimo lo va a intentar pasar como parametro, en ese caso debo poner esta nueva funciona arriba de la que espera parametro
async def users(v_id: int, response: Response):
    try:
        c_usuarios = d_unusuario(connection,v_id)
        if c_usuarios == None:
           response.status_code = 404
           return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
        else:
            return {"datos": c_usuarios}
    except Exception as ex:
        print("Error al consultar usuario", ex)

# delete un usuario
@router.delete("/")
async def users(v_id: int,response: Response):
    try:
        c_usuarios = d_unusuario(connection,v_id)
        if c_usuarios == None:
           response.status_code = 404
           return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
        else:
            v_actualizo = d_eliminarusuario(connection,v_id)
            if v_actualizo == False:
                return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
            else:
                response.status_code = 204      # se devuelve solo este estado existoso
    except Exception as ex:
        print("Error al dar de baja un usuario", ex)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def users(v_usuario: e_usuario):
    try:
        # Extraer los valores en el orden adecuado
        v_id=0
        c_usuarios = d_unusuario(connection,v_id)
        if c_usuarios != None:
            Response.status_code = 404
            return {"Atención": f"El usuario {v_id} ya existe"}
        else:
            usuario_dict = v_usuario.model_dump()
            v_parametros = [
                usuario_dict["apellynom"],
                usuario_dict["clave"],
                usuario_dict["cod_ofi"],
                usuario_dict["fecha_alta"],
                usuario_dict["usuario"],
                usuario_dict["baja"],
                usuario_dict["cod_sis4"]
            ]
            d_insertarusuario(connection,v_parametros)
            return {"message": "Usuario creado exitosamente", "usuario": v_usuario}

    except Exception as e:
        Response.status_code = 500
        return {"error": str(e)}

@router.put("/")
async def users(v_id: int, v_usuario: e_usuario, response: Response, response_model=e_usuarioresp):
    try:
        c_usuarios = d_unusuario(connection, v_id)
        if c_usuarios is None:
            response.status_code = 404
            return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
        else:
            usuario_dict = v_usuario.dict()
            v_parametros = [
                usuario_dict["apellynom"],
                usuario_dict["clave"],
                usuario_dict["cod_ofi"],
                usuario_dict["fecha_alta"],
                usuario_dict["usuario"],
                usuario_dict["baja"],
                usuario_dict["cod_sis4"]
            ]

            v_actualizo = d_actualizarusuario(connection, v_parametros, v_id)
            if not v_actualizo:
                return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
            else:
                #response.status_code = 204 # si uso body no puedo mandar esto porque no permite respuesta
                return e_usuarioresp(codigo=v_id, fecha_actu=datetime.date(datetime.now()))

    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}
