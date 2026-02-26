from fastapi import APIRouter, Response, status
from conexion import DAO
from entidades import e_venta
import sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from d_ventas import *

dao = DAO()
connection = dao.connection

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.get("/")
async def listar_ventas(response: Response):
    try:
        datos = d_listar_ventas(connection)
        return {"datos": datos}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.get("/{codigo}")
async def una_venta(codigo: int, response: Response):
    try:
        dato = d_unaventa(connection, codigo)
        if dato is None:
            response.status_code = 404
            return {"error": f"Venta {codigo} no encontrada"}
        return {"datos": dato}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_venta(v_venta: e_venta, response: Response):
    try:
        nuevo_id = d_insertar_venta(
            connection,
            v_venta.cod_cliente,
            v_venta.observaciones,
            v_venta.detalle,
            v_venta.pagos
        )
        if nuevo_id is None:
            response.status_code = 500
            return {"error": "Error al registrar la venta"}
        return {"codigo": nuevo_id, "mensaje": "Venta registrada correctamente"}
    except Exception as ex:
        response.status_code = 500
        return {"error": str(ex)}