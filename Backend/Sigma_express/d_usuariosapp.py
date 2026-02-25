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
from varios import * # type: ignore # type: ignore
# from varios import *
# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')


def d_listarusuariosapp(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuariosapp order by codigo;")            
            v_tabla = cursor.fetchall()
            total_usuarios = len(v_tabla)
            cursor.close()
            # print("Total de usuarios: ", total_usuarios)
            return v_tabla
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos", ex)

def d_unusuarioappcodigo(connection, v_parametros):
    if connection:
        try:
            cursor = connection.cursor()                
            v_texto = "SELECT email,password FROM usuariosapp WHERE baja = False and codigo = %s;"                               
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
            print("Error al consultar a la Base de Datos de usuarios de la App", ex)
            
def d_unusuarioapp(connection, v_parametros):
    if connection:
        try:
            cursor = connection.cursor()                
            v_texto = "SELECT email,password,codigo FROM usuariosapp WHERE baja = False AND email = %s;"                               
            
            #v_parametros va sin [] al ser un item
            if not isinstance(v_parametros, tuple):
               v_parametros = (v_parametros,)            

            cursor.execute(v_texto, (v_parametros))                                    
            #print(v_texto % v_parametros,)
            v_tabla = cursor.fetchone()
            cursor.close()
            if v_tabla:
                return v_tabla
            else:
                return None
        except (Exception, psycopg2.Error) as ex:
            print("Error al consultar a la Base de Datos de usuarios de la App", ex)


def d_insertarusuarioapp(connection, v_parametros):
    if connection:
        try:
            #print(v_parametros)
            cursor = connection.cursor()                                                     
            v_texto = """
                INSERT INTO usuariosapp (email,password,apellido,nombres,direccion_fac,localidad_fac,cod_postal_fac,provincia_fac,telefono,direccion_env,localidad_env,cod_postal_env,provincia_env,fecha_alta,baja,tipo_doc,nro_doc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING codigo;
            """                                                
            print(v_texto)
            cursor.execute(v_texto, (v_parametros[0], v_parametros[1], v_parametros[2], v_parametros[3], v_parametros[4], v_parametros[5], v_parametros[6], v_parametros[7], v_parametros[8], v_parametros[9], v_parametros[10], v_parametros[11], v_parametros[12], v_parametros[13], v_parametros[14], v_parametros[15], v_parametros[16]))            
            
            v_nuevoid = cursor.fetchone()[0]
            connection.commit()
            print(f"Registro insertado con ID: {v_nuevoid}")
            return v_nuevoid
        except (Exception, psycopg2.Error) as ex:
            print("Error al insertar en la Base de Datos", ex)

def d_eliminarusuarioapp(connection, v_codigo):
    if connection:
        try:
            cursor = connection.cursor()
            # Llamar a la función PostgreSQL fn_eliminausuario() con la tupla que contiene el codigo
            cursor.callproc('fn_eliminausuarioapp', (v_codigo,))
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
