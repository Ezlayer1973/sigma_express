import sys, os
from datetime import datetime
from fastapi import FastAPI, Response, status, Body, APIRouter, Depends
from decouple import config

# Asegúrate de que backend esté en sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from oauth2 import *
from conexion import DAO
from d_expedientes import *
from d_usuariosapp import *
from entidades import *

# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import *

# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')

dao=DAO()
connection = dao.connection
router = APIRouter(
    prefix="/expedientes",
    tags=['Expedientes online']
) 

@router.get("/")
async def expedientes(response: Response):  # Se eliminó 'v_logueado: int = Depends(get_current_user)'
    try:
        c_expedientes = d_listarexpedientes(connection)      
        return {"datos": c_expedientes}
    except Exception as ex:
        print("Error al consultar expedientes", ex)
        response.status_code = 500
        return {"error": "Error al consultar expedientes"}

        
# un usuario
@router.get("/{v_nro_expe}")    #cuando uso parametros por path debo tener cuidado. si creo una subpagina /userpath/ultimo por ej, ultimo lo va a intentar pasar como parametro, en ese caso debo poner esta nueva funciona arriba de la que espera parametro
async def userapp(v_nro_expe: int, response: Response): #, v_logueado: int = Depends(get_current_user)):
    try:        
        c_expedientes = d_unexpedienteapp(connection,v_nro_expe)
        if c_expedientes == None:
           response.status_code = 404
           connection.rollback()  # type: ignore # Descartar la transacción abortada
           return {"Atención": f"El expediente {v_nro_expe} no existe o fue dado de baja"}
        else:    
            return {"datos": c_expedientes}        
    except Exception as ex:
        v_roll = connection.rollback()  # Descartar la transacción abortada        
        print("Error al consultar un expediente", ex)        

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createuser_app(v_usuarioapp: e_usuarioapp, response: Response):    
    try:
        # Verifica si el usuario ya existe
        usuariocargado_dict = v_usuarioapp.model_dump()
        v_parametros = [
            usuariocargado_dict["email"],
            usuariocargado_dict["password"]               
        ]                
        
        c_usuarios = d_unusuarioapp(connection,v_parametros[0],) 
        if c_usuarios is not None:
            response.status_code = status.HTTP_404_NOT_FOUND
            connection.rollback()  # Descartar la transacción abortada                    
            return {"Atención": f"El usuario con este email {v_parametros[0],} ya existe"}
        else:
            v_key = str_to_key(v_llave) # llave para el hash
            usuario_dict = v_usuarioapp.model_dump()            
            v_parametros = [
                usuario_dict["email"],
                byte_to_str(encripta(usuario_dict["password"],v_key)), #encripto
                usuario_dict["apellido"],
                usuario_dict["nombres"],
                usuario_dict["direccion_fac"],
                usuario_dict["localidad_fac"],
                usuario_dict["cod_postal_fac"],
                usuario_dict["provincia_fac"],
                usuario_dict["telefono"],                
                usuario_dict["direccion_env"],
                usuario_dict["localidad_env"],
                usuario_dict["cod_postal_env"],
                usuario_dict["provincia_env"],                
                usuario_dict["fecha_alta"],
                usuario_dict["baja"],                     
                usuario_dict["tipo_doc"],
                usuario_dict["nro_doc"]                                     
                ]
            
            nuevo_id = d_insertarusuarioapp(connection, v_parametros)            
            if nuevo_id is None:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                connection.rollback()  # Descartar la transacción abortada                                    
                return {"Error": "Error al insertar en la base de datos"}
            
            # Crear la respuesta con la fecha actual
            usuarioresp_dict = {
                "codigo": nuevo_id,
                "fecha_alta": datetime.now()
            }
            return usuarioresp_dict
        
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}                             


# delete usuariosapp, todos!
@router.delete("/")
async def userapp(v_id: int,response: Response, v_logueado: int = Depends(get_current_user)):
    try:
        c_usuarios = d_unusuarioappcodigo(connection,v_id)
        if c_usuarios == None:
           response.status_code = 404
           return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
        else:
            v_actualizo = d_eliminarusuarioapp(connection,v_id)
            if v_actualizo == False:
                return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
            else:
                response.status_code = 204      # se devuelve solo este estado existoso
    except Exception as ex:
        print("Error al dar de baja un usuario", ex)