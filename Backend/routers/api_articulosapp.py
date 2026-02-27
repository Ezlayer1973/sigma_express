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
from d_articulosapp import *
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
    prefix="/articulosapp",
    tags=['Articulos Online']
) 

@router.get("/")
async def articulosapp(response: Response, v_logueado: int = Depends(get_current_user)):              #name function thats no matter
    try:
        
        c_articulos = d_listararticulosapp(connection)      
        return {"datos": c_articulos}
    except Exception as ex:
        print("Error al consultar articulos", ex)
        
# un usuario
@router.get("/{v_codigo}")    #cuando uso parametros por path debo tener cuidado. si creo una subpagina /userpath/ultimo por ej, ultimo lo va a intentar pasar como parametro, en ese caso debo poner esta nueva funciona arriba de la que espera parametro
async def articuloapp(v_codigo: str, response: Response, v_logueado: int = Depends(get_current_user)):
    try:        
        c_articulos = d_unarticuloappcodigo(connection,v_codigo)
        if c_articulos == None:
           response.status_code = 404
           connection.rollback()  # type: ignore # Descartar la transacción abortada
           return {"Atención": f"El articulo {v_codigo} no existe o fue dado de baja"}
        else:    
            return {"datos": c_articulos}        
    except Exception as ex:
        v_roll = connection.rollback()  # Descartar la transacción abortada        
        print("Error al consultar articulos", ex)        

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createarticulo_app(v_articuloapp: e_articuloapp, response: Response):    
    try:
        # Verifica si el usuario ya existe
        articulocargado_dict = v_articuloapp.model_dump()
        v_parametros = [
            articulocargado_dict["codigo"],
            articulocargado_dict["descri"]               
        ]                
        
        c_articulos = d_unarticuloappcodigo(connection,v_parametros[0],) 
        if c_articulos is not None:
            response.status_code = status.HTTP_404_NOT_FOUND
            connection.rollback()  # Descartar la transacción abortada                    
            return {"Atención": f"El articulo con este código {v_parametros[0],} ya existe"}
        else:
            # v_key = str_to_key(v_llave) # llave para el hash
            articulo_dict = v_articuloapp.model_dump()            
            v_parametros = [         
                articulo_dict["codigo"],                   
                articulo_dict["descri"]                                     
                ]
            
            nuevo_id = d_insertararticuloapp(connection, v_parametros)            
            if nuevo_id is None:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                connection.rollback()  # Descartar la transacción abortada                                    
                return {"Error": "Error al insertar en la base de datos"}
            
            # Crear la respuesta con la fecha actual
            articuloresp_dict = {
                "codigo": nuevo_id,
                "fecha_alta": datetime.now()
            }
            return articuloresp_dict
        
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}                             


# delete usuariosapp, todos!
@router.delete("/")
async def articuloapp(v_id: int,response: Response, v_logueado: int = Depends(get_current_user)):
    try:
        c_articulos = d_unarticuloappcodigo(connection,v_id)
        if c_articulos == None:
           response.status_code = 404
           return {"Atención": f"El articulo {v_id} no existe o fue dado de baja"}
        else:
            v_actualizo = d_eliminararticuloapp(connection,v_id)
            if v_actualizo == False:
                return {"Atención": f"El articulo {v_id} no existe o fue dado de baja"}
            else:
                response.status_code = 204      # se devuelve solo este estado existoso
    except Exception as ex:
        print("Error al dar de baja un articulo", ex)