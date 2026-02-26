import psycopg2

def d_listar_articulos(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.codigo, a.descripcion, a.cod_rubro, r.descripcion as rubro,
                   a.precio, a.codigo_barra, a.fecha_alta, a.baja
            FROM articulos a
            LEFT JOIN rubros r ON a.cod_rubro = r.codigo
            WHERE a.baja = false ORDER BY a.descripcion;
        """)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al listar artículos", ex)

def d_unarticulo(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.codigo, a.descripcion, a.cod_rubro, r.descripcion as rubro,
                   a.precio, a.codigo_barra, a.fecha_alta, a.baja
            FROM articulos a
            LEFT JOIN rubros r ON a.cod_rubro = r.codigo
            WHERE a.codigo = %s;
        """, (codigo,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al buscar artículo", ex)

def d_insertar_articulo(connection, v):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO articulos (descripcion, cod_rubro, precio, codigo_barra, fecha_alta, baja)
            VALUES (%s, %s, %s, %s, CURRENT_DATE, false) RETURNING codigo;
        """, (v[0], v[1], v[2], v[3]))
        nuevo_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return nuevo_id
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al insertar artículo", ex)

def d_actualizar_articulo(connection, codigo, v):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE articulos SET descripcion=%s, cod_rubro=%s, precio=%s, codigo_barra=%s
            WHERE codigo=%s;
        """, (v[0], v[1], v[2], v[3], codigo))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al actualizar artículo", ex)
        return False

def d_eliminar_articulo(connection, codigo):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE articulos SET baja = true WHERE codigo = %s;", (codigo,))
        connection.commit()
        cursor.close()
        return True
    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al eliminar artículo", ex)
        return False