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

def d_listarusuarios(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios order by codigo;")            
            v_tabla = cursor.fetchall()
            total_usuarios = len(v_tabla)
            cursor.close()
            # print("Total de usuarios: ", total_usuarios)
            return v_tabla
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos", ex)

def d_unusuario(connection, v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            v_texto = "SELECT * FROM usuarios WHERE baja = False and codigo = %s;"
            cursor.execute(v_texto, (v_codigo,))
            v_tabla = cursor.fetchone()
            cursor.close()
            if v_tabla:
                return v_tabla
            else:
                return None
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos Un Usuario", ex)

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
            
def d_unusuario_login(connection, v_usuario):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT codigo, apellynom, clave, usuario
                FROM usuarios
                WHERE baja = False AND usuario = %s;
            """, (v_usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except (Exception, psycopg2.Error) as ex:
            print("Error al buscar usuario para login", ex)
            return None            
