
# conexion.py
import psycopg2
from typing import Optional
from decouple import config

class DAO:
    def __init__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                host=config('PO_host'),
                user=config('PO_user'),
                password=config('PO_password'),                
                dbname=config('PO_dbname'),
                port=config('PO_port')

                # dbname="inventario",
                # user="sigma",
                # password="proliant",
                # host="192.168.1.22",
                # port="5432"
            )
        except psycopg2.Error as e:
            print("Error al intentar la conexión con el motor de Base de Datos", e)
    
    def close(self):
        if self.connection:
            self.connection.close()
