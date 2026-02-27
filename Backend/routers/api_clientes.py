from fastapi import APIRouter, Response, status
from conexion import DAO
from entidades import e_cliente
import sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from d_clientes import *

dao = DAO()
connection = dao.connection

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
async def listar_clientes(response: Response):
    try:
        datos = d_listar_clientes(connection)
        return {"datos": datos}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.get("/{codigo}")
async def un_cliente(codigo: int, response: Response):
    try:
        dato = d_uncliente(connection, codigo)
        if dato is None:
            response.status_code = 404
            return {"error": f"Cliente {codigo} no encontrado"}
        return {"datos": dato}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_cliente(v_cli: e_cliente, response: Response):
    try:
        params = [v_cli.apellynom, v_cli.tipo_doc, v_cli.nro_doc,
                  v_cli.telefono, v_cli.email, v_cli.direccion]
        nuevo_id = d_insertar_cliente(connection, params)
        if nuevo_id is None:
            response.status_code = 500
            return {"error": "Error al insertar"}
        return {"codigo": nuevo_id}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.put("/{codigo}")
async def actualizar_cliente(codigo: int, v_cli: e_cliente, response: Response):
    try:
        params = [v_cli.apellynom, v_cli.tipo_doc, v_cli.nro_doc,
                  v_cli.telefono, v_cli.email, v_cli.direccion]
        ok = d_actualizar_cliente(connection, codigo, params)
        if not ok:
            response.status_code = 500
            return {"error": "Error al actualizar"}
        return {"mensaje": "Actualizado correctamente"}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.delete("/{codigo}")
async def eliminar_cliente(codigo: int, response: Response):
    try:
        ok = d_eliminar_cliente(connection, codigo)
        if not ok:
            response.status_code = 500
            return {"error": "Error al eliminar"}
        response.status_code = 204
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}