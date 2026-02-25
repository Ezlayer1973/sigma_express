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
from d_pedidosapp import *
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
    prefix="/pedidos",
    tags=['Pedidos online']
) 

@router.get("/")
async def pedidosapp(response: Response, v_logueado: int = Depends(get_current_user)):
    try:        
        print(v_logueado)
        c_pedidos = d_listarpedidosapp(connection)      
        return {"datos": c_pedidos}
    except Exception as ex:
        print("Error al consultar usuarios", ex)           

@router.post("/", status_code=status.HTTP_201_CREATED)
async def pedidosapp(v_usuarioapp: e_pedidos, response: Response, v_logueado: int = Depends(get_current_user)):    
    try:
        # Traigo ultimo numero de pedido de esa sucursal
        # Ejemplo de uso
        v_sucursal = 1  # Supongamos que esta es la sucursal para la cual quieres obtener el siguiente número
        v_nro_comp = obtener_ultimo_nro_comp(connection, v_sucursal)        
        pedidocargado_dict = v_usuarioapp.model_dump()
        pedidocargado_dict["cod_usuapp"] = v_logueado
        pedidocargado_dict["nro_comp"] = v_nro_comp
        v_parametros = [
            pedidocargado_dict["id"],
            pedidocargado_dict["cod_cli"],
            pedidocargado_dict["fecha"],
            pedidocargado_dict["hora"],
            pedidocargado_dict["nro_comp"],
            pedidocargado_dict["baja"],
            pedidocargado_dict["letra"],
            pedidocargado_dict["sucursal"],
            pedidocargado_dict["cod_usuapp"]            
        ]                
        
        c_pedidos = d_unpedidoapp(connection,v_parametros[0],) 
        if c_pedidos is not None:
            response.status_code = status.HTTP_404_NOT_FOUND
            connection.rollback()  # Descartar la transacción abortada                    
            return {"Atención": f"El pedido {v_parametros[0],} ya existe"}
        else:                        
            nuevo_id = d_insertarpedidoapp(connection, v_parametros)            
            if nuevo_id is None:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                connection.rollback()  # Descartar la transacción abortada                                    
                return {"Error": "Error al insertar en la base de datos"}            
            
            # Crear la respuesta con la fecha actual
            pedidoresp_dict = {
                "codigo": nuevo_id,
                "fecha_alta": datetime.now()
            }
            return pedidoresp_dict
        
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}                             


# delete usuariosapp, todos!
@router.delete("/")
async def pedidosapp(v_id: int,response: Response, v_logueado: int = Depends(get_current_user)):
    try:
        c_pedidos = d_unpedidoappcodigo(connection,v_id)
        print(c_pedidos)
        if c_pedidos == None:
           response.status_code = 404
           return {"Atención": f"El pedido {v_id} no existe o fue dado de baja"}
        else:
            if v_logueado == c_pedidos[0]:
                v_actualizo = d_eliminarpedido(connection,v_id)
                if v_actualizo == False:
                   response.status_code = 403
                   connection.rollback()  # Descartar la transacción abortada                                    
                   return {"Atención": f"Hubo un problema al dar de baja el pedido {v_id}"}                    
                else:
                    response.status_code = 204      # se devuelve solo este estado existoso
            else:
                response.status_code = 403
                return {"Atención": f"El pedido {v_id} existe pero no es suyo"}                    
    except Exception as ex:
        print("Error al eliminar el pedido", ex)
         