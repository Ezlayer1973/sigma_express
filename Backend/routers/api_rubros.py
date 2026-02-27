from fastapi import APIRouter, Response, status
from conexion import DAO
from entidades import e_rubro
import sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from d_rubros import *

dao = DAO()
connection = dao.connection

router = APIRouter(prefix="/rubros", tags=["Rubros"])

@router.get("/")
async def listar_rubros(response: Response):
    try:
        datos = d_listar_rubros(connection)
        return {"datos": datos}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.get("/{codigo}")
async def un_rubro(codigo: int, response: Response):
    try:
        dato = d_unrubro(connection, codigo)
        if dato is None:
            response.status_code = 404
            return {"error": f"Rubro {codigo} no encontrado"}
        return {"datos": dato}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_rubro(v_rubro: e_rubro, response: Response):
    try:
        nuevo_id = d_insertar_rubro(connection, v_rubro.descripcion)
        if nuevo_id is None:
            response.status_code = 500
            return {"error": "Error al insertar"}
        return {"codigo": nuevo_id}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.put("/{codigo}")
async def actualizar_rubro(codigo: int, v_rubro: e_rubro, response: Response):
    try:
        ok = d_actualizar_rubro(connection, codigo, v_rubro.descripcion)
        if not ok:
            response.status_code = 500
            return {"error": "Error al actualizar"}
        return {"mensaje": "Actualizado correctamente"}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.delete("/{codigo}")
async def eliminar_rubro(codigo: int, response: Response):
    try:
        ok = d_eliminar_rubro(connection, codigo)
        if not ok:
            response.status_code = 500
            return {"error": "Error al eliminar"}
        response.status_code = 204
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}