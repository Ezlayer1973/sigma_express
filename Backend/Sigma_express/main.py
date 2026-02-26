#region IMPORTACIONES, CABECERA Y CONEXION
import sys, os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Response, status, Body
from fastapi.middleware.cors import CORSMiddleware
#import conexion, entidades,d_usuarios,d_usuariosapp
from decouple import config
from routers import api_expedientes
from routers import api_usuarios, api_auth,api_pedidos
import conexion, d_usuarios, entidades
from conexion import DAO


# Cabecera estándar
libreria_path = config('PO_libreria')
if libreria_path not in sys.path:
    sys.path.append(libreria_path)
from varios import * # type: ignore

# from varios import *
# Traigo variables de entorno que igual deberé importar arriba en cada .py:
v_pathserver = os.getenv('PATHSERVER')
v_llave = config('PO_')

# Creo conexión
dao = DAO()

# Creo app
app = FastAPI()

# Configuración de CORS
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a ["http://127.0.0.1"] o el dominio de tu frontend si prefieres limitar el acceso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.include_router(api_usuarios.router)
from routers import api_expedientes, api_rubros, api_articulos, api_clientes, api_ventas

app.include_router(api_expedientes.router)
app.include_router(api_rubros.router)
app.include_router(api_articulos.router)
app.include_router(api_clientes.router)
app.include_router(api_ventas.router)
#app.include_router(api_auth.router)
#app.include_router(api_pedidos.router)
#endregion

# Definir función de cierre de conexión
def cerrarconexion():
    dao.close()  # Cerrar la conexión al salir

def menuPrincipal():        
    v_continuar = True
    while v_continuar:
        v_opcioncorrecta = False
        while not v_opcioncorrecta:
            print(dtoc(date()), mitime())
            print("------------- Menú Principal -------------")
            print("0.- Salir")            
            print("1.- Api Expedientes")
            print("-----------------------------------------")
            
            v_opcion = int(input("Seleccione una opción: "))
            if v_opcion < 0 or v_opcion > 1:
                v_opcioncorrecta = False
                print("Opción incorrecta!!")

            elif v_opcion == 0:
                v_continuar = False
                print("Nos vemos!")
                cerrarconexion()                
                break

            else:
                v_opcioncorrecta = True
                if v_opcion == 1:
                    try:
                        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
                    except Exception as ex:
                        print("Error al iniciar servidor de aplicaciones", ex)                
                else:
                    print(v_opcion)

if __name__ == "__main__":
    menuPrincipal()
