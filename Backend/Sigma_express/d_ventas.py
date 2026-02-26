import psycopg2

def d_insertar_venta(connection, cod_cliente, observaciones, detalle, pagos):
    try:
        cursor = connection.cursor()

        # 1. Insertar cabecera
        cursor.execute("""
            INSERT INTO ventas (cod_cliente, observaciones, total, estado, baja)
            VALUES (%s, %s, 0, 'confirmada', false) RETURNING codigo;
        """, (cod_cliente, observaciones))
        cod_venta = cursor.fetchone()[0]

        # 2. Insertar detalle y calcular total
        total = 0
        for item in detalle:
            subtotal = item.cantidad * item.precio_unitario
            total += subtotal
            cursor.execute("""
                INSERT INTO ventas_detalle (cod_venta, cod_articulo, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s);
            """, (cod_venta, item.cod_articulo, item.cantidad, item.precio_unitario, subtotal))

        # 3. Actualizar total en cabecera
        cursor.execute("UPDATE ventas SET total = %s WHERE codigo = %s;", (total, cod_venta))

        # 4. Insertar pagos
        for pago in pagos:
            cursor.execute("""
                INSERT INTO ventas_pagos (cod_venta, forma_pago, monto, nro_tarjeta, cuotas)
                VALUES (%s, %s, %s, %s, %s);
            """, (cod_venta, pago.forma_pago, pago.monto, pago.nro_tarjeta, pago.cuotas))

        connection.commit()
        cursor.close()
        return cod_venta

    except (Exception, psycopg2.Error) as ex:
        connection.rollback()
        print("Error al insertar venta", ex)
        return None

def d_listar_ventas(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT v.codigo, v.fecha, c.apellynom, v.total, v.estado
            FROM ventas v
            LEFT JOIN clientes c ON v.cod_cliente = c.codigo
            WHERE v.baja = false ORDER BY v.fecha DESC LIMIT 100;
        """)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    except (Exception, psycopg2.Error) as ex:
        print("Error al listar ventas", ex)

def d_unaventa(connection, codigo):
    try:
        cursor = connection.cursor()
        # Cabecera
        cursor.execute("""
            SELECT v.codigo, v.fecha, v.cod_cliente, c.apellynom, v.total, v.estado, v.observaciones
            FROM ventas v LEFT JOIN clientes c ON v.cod_cliente = c.codigo
            WHERE v.codigo = %s;
        """, (codigo,))
        cabecera = cursor.fetchone()

        # Detalle
        cursor.execute("""
            SELECT d.cod_articulo, a.descripcion, d.cantidad, d.precio_unitario, d.subtotal
            FROM ventas_detalle d
            JOIN articulos a ON d.cod_articulo = a.codigo
            WHERE d.cod_venta = %s;
        """, (codigo,))
        detalle = cursor.fetchall()

        # Pagos
        cursor.execute("""
            SELECT forma_pago, monto, nro_tarjeta, cuotas
            FROM ventas_pagos WHERE cod_venta = %s;
        """, (codigo,))
        pagos = cursor.fetchall()

        cursor.close()
        return {"cabecera": cabecera, "detalle": detalle, "pagos": pagos}
    except (Exception, psycopg2.Error) as ex:
        print("Error al buscar venta", ex)