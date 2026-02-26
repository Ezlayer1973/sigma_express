from fastapi import APIRouter, Response, status
from conexion import DAO
from entidades import e_articulo
import sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from d_articulos import *

dao = DAO()
connection = dao.connection

router = APIRouter(prefix="/articulos", tags=["Artículos"])

@router.get("/")
async def listar_articulos(response: Response):
    try:
        datos = d_listar_articulos(connection)
        return {"datos": datos}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.get("/{codigo}")
async def un_articulo(codigo: int, response: Response):
    try:
        dato = d_unarticulo(connection, codigo)
        if dato is None:
            response.status_code = 404
            return {"error": f"Artículo {codigo} no encontrado"}
        return {"datos": dato}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_articulo(v_art: e_articulo, response: Response):
    try:
        params = [v_art.descripcion, v_art.cod_rubro, v_art.precio, v_art.codigo_barra]
        nuevo_id = d_insertar_articulo(connection, params)
        if nuevo_id is None:
            response.status_code = 500
            return {"error": "Error al insertar"}
        return {"codigo": nuevo_id}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.put("/{codigo}")
async def actualizar_articulo(codigo: int, v_art: e_articulo, response: Response):
    try:
        params = [v_art.descripcion, v_art.cod_rubro, v_art.precio, v_art.codigo_barra]
        ok = d_actualizar_articulo(connection, codigo, params)
        if not ok:
            response.status_code = 500
            return {"error": "Error al actualizar"}
        return {"mensaje": "Actualizado correctamente"}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.delete("/{codigo}")
async def eliminar_articulo(codigo: int, response: Response):
    try:
        ok = d_eliminar_articulo(connection, codigo)
        if not ok:
            response.status_code = 500
            return {"error": "Error al eliminar"}
        response.status_code = 204
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}