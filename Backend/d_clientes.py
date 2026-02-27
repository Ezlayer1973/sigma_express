import psycopg2
from datetime import date

def d_listar_clientes(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT codigo, apellynom, tipo_doc, nro_doc, telefono, email, direccion, fecha_alta, baja
            FROM clientes WHERE baja = false ORDER BY apellynom;
        """)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al listar clientes", ex)

def d_uncliente(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT codigo, apellynom, tipo_doc, nro_doc, telefono, email, direccion, fecha_alta, baja
            FROM clientes WHERE codigo = %s;
        """, (codigo,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al buscar cliente", ex)

def d_insertar_cliente(connection, v):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO clientes (apellynom, tipo_doc, nro_doc, telefono, email, direccion, fecha_alta, baja)
            VALUES (%s, %s, %s, %s, %s, %s, %s, false) RETURNING codigo;
        """, (v[0], v[1], v[2], v[3], v[4], v[5], date.today()))
        nuevo_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return nuevo_id
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al insertar cliente", ex)

def d_actualizar_cliente(connection, codigo, v):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE clientes SET apellynom=%s, tipo_doc=%s, nro_doc=%s,
            telefono=%s, email=%s, direccion=%s WHERE codigo=%s;
        """, (v[0], v[1], v[2], v[3], v[4], v[5], codigo))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al actualizar cliente", ex)
        return False

def d_eliminar_cliente(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET baja = true WHERE codigo = %s;", (codigo,))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al eliminar cliente", ex)
        return False