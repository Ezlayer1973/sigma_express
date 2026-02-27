import sys,os
import psycopg2
from typing import Optional
from conexion import DAO
from datetime import datetime
from decouple import config

# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import * # type: ignore # type: ignore
# from varios import *
# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')


def d_listarpedidosapp(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pedidos order by fecha;")            
            v_tabla = cursor.fetchall()
            total_usuarios = len(v_tabla)
            cursor.close()
            # print("Total de usuarios: ", total_usuarios)
            return v_tabla
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos", ex)

def d_unpedidoappcodigo(connection, v_parametros):
    if connection:
        try:
            cursor = connection.cursor()                
            v_texto = "SELECT id,cod_usuapp FROM pedidos WHERE baja = False and id = %s;"                               
            if not isinstance(v_parametros, tuple):
                v_parametros = (v_parametros,)                            
            cursor.execute(v_texto, v_parametros)
            #print(v_texto,v_parametros,)
            v_tabla = cursor.fetchone()            
            cursor.close()
            if v_tabla:
                return v_tabla
            else:
                return None
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos de pedidos Online", ex)
            
def d_unpedidoapp(connection, v_parametros):
    pass
    # if connection:
    #     try:
    #         cursor = connection.cursor()                
    #         v_texto = "SELECT email, password FROM usuariosapp WHERE baja = False AND email = %s;"                               
            
    #         #v_parametros va sin [] al ser un item
    #         if not isinstance(v_parametros, tuple):
    #            v_parametros = (v_parametros,)            

    #         cursor.execute(v_texto, (v_parametros))                                    
    #         print(v_texto % v_parametros,)
    #         v_tabla = cursor.fetchone()
    #         cursor.close()
    #         if v_tabla:
    #             return v_tabla
    #         else:
    #             return None
    #     except (Exception, psycopg2.Error) as ex:
    #         print("Error al consultar a la Base de Datos de usuarios de la App", ex)


def d_insertarpedidoapp(connection, v_parametros):
    if connection:
        try:
            cursor = connection.cursor()            
            v_texto = """
                INSERT INTO pedidos (cod_cli,fecha,hora,nro_comp,baja,letra,sucursal,cod_usuapp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id; 
            """                        
            cursor.execute(v_texto, (v_parametros[1],
                                    v_parametros[2],
                                    v_parametros[3],
                                    v_parametros[4],
                                    v_parametros[5],
                                    v_parametros[6],
                                    v_parametros[7],
                                    v_parametros[8])) 
                                   
            v_nuevoid = cursor.fetchone()[0]
            connection.commit()
            print(f"Registro insertado con ID: {v_nuevoid}")
            return v_nuevoid
        except (Exception, psycopg2.Error) as ex:
            print("Error al insertar en la Base de Datos", ex)


def d_eliminarpedido(connection, v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            # Llamar a la función PostgreSQL fn_eliminausuario() con la tupla que contiene el codigo
            cursor.callproc('fn_eliminapedido', (v_codigo,))
            connection.commit()            
            # Ejemplo de cómo obtener el resultado si la función devuelve algo            
            print(f"Registro con ID {v_codigo} dado de baja correctamente")
            return True

        except (Exception, psycopg2.Error) as ex:
            print("Error al eliminar en la Base de Datos", ex)
            connection.rollback()  # Revertir cambios en caso de error
            return False

        finally:
            cursor.close()


def obtener_ultimo_nro_comp(connection, sucursal_id):
    query = """
    SELECT MAX(nro_comp) AS ultimo_nro_comp
    FROM pedidos
    WHERE sucursal = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (sucursal_id,))
        result = cursor.fetchone()
        ultimo_nro_comp = result[0] if result[0] is not None else 0
        return ultimo_nro_comp + 1  # Retornar el siguiente número de pedido