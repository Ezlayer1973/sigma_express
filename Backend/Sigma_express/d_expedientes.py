import sys,os
import psycopg2
from typing import Optional
from conexion import DAO
from datetime import datetime
import base64 # convertir fernet en texto
from decouple import config


# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import * # type: ignore

# from varios import *
# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')

# Obtiene una lista de los 100 expedientes más recientes de la base de datos.
def d_listarexpedientes(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT fecha,concepto,iniciador,doc_inic,estado,fecha_actu,cod_ofiactual,baja,codigo,numero FROM expedientes order by fecha desc limit 100;")         
            v_tabla = cursor.fetchall()
            total_usuarios = len(v_tabla)
            cursor.close()
            # print("Total de usuarios: ", total_usuarios)
            return v_tabla
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos", ex)

# Busca y retorna los datos de un expediente específico por su número, si no está dado de baja.
def d_unexpedienteapp(connection, v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            v_texto = "SELECT fecha,concepto,iniciador,doc_inic,estado,fecha_actu,cod_ofiactual,baja,codigo,numero FROM expedientes WHERE baja = False and numero = %s;"
            cursor.execute(v_texto, (v_codigo,))
            v_tabla = cursor.fetchone()
            cursor.close()
            if v_tabla:
                return v_tabla
            else:
                return None
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos Un Usuario", ex)

# Inserta un nuevo usuario en la base de datos y retorna el ID generado.
def d_insertarusuario(connection, v_parametros):
    if connection:
        try:
            cursor = connection.cursor()
            print(v_parametros)
            v_texto = """
                INSERT INTO usuarios (apellynom, clave, cod_ofi, fecha_alta, usuario, baja, cod_sis4)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING codigo;
            """
            cursor.execute(v_texto, (v_parametros[0], v_parametros[1], v_parametros[2], v_parametros[3], v_parametros[4], v_parametros[5], v_parametros[6]))
            v_nuevoid = cursor.fetchone()[0]
            connection.commit()
            print(f"Registro insertado con ID: {v_nuevoid}")
            return v_nuevoid
        except (Exception, psycopg2.Error) as ex:
            print("Error al insertar en la Base de Datos", ex)


# Actualiza los datos de un usuario existente identificado por su código.
def d_actualizarusuario(connection, v_parametros,v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            v_texto = """
                UPDATE usuarios SET apellynom = %s, clave = %s,cod_ofi = %s,fecha_alta = %s,usuario = %s,baja = %s,cod_sis4 = %s WHERE codigo = %s;
            """
            cursor.execute(v_texto, (v_parametros[0], v_parametros[1], v_parametros[2], v_parametros[3], v_parametros[4], v_parametros[5], v_parametros[6],v_codigo))                        
            connection.commit()            
            print("Registro actualizado ")
            return True

        except (Exception, psycopg2.Error) as ex:
            print("Error al actualizar en la Base de Datos", ex)
            return False

# Da de baja (elimina lógicamente) un usuario en la base de datos usando una función de PostgreSQL.
def d_eliminarusuario(connection, v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            # Llamar a la función PostgreSQL fn_eliminausuario() con la tupla que contiene el codigo
            cursor.callproc('fn_eliminausuario', (v_codigo,))
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
