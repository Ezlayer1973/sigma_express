import psycopg2

def d_listar_rubros(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT codigo, descripcion, baja FROM rubros WHERE baja = false ORDER BY descripcion;")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al listar rubros", ex)

def d_unrubro(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT codigo, descripcion, baja FROM rubros WHERE codigo = %s;", (codigo,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al buscar rubro", ex)

def d_insertar_rubro(connection, descripcion):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rubros (descripcion, baja) VALUES (%s, false) RETURNING codigo;", (descripcion,))
        nuevo_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return nuevo_id
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al insertar rubro", ex)

def d_actualizar_rubro(connection, codigo, descripcion):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE rubros SET descripcion = %s WHERE codigo = %s;", (descripcion, codigo))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al actualizar rubro", ex)
        return False

def d_eliminar_rubro(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE rubros SET baja = true WHERE codigo = %s;", (codigo,))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al eliminar rubro", ex)
        return False