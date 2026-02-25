# #******************************************************************
# #region IMPORTACIONES, CABECERA Y CONEXION1
# import sys, os
# from datetime import datetime
# from fastapi import FastAPI, Response, status, Body
# #from pydantic import BaseModel
# from conexion import DAO
# from decouple import config
# # from d_usuarios import *
# # from d_usuariosapp import *
# # from entidades import e_usuario,e_usuarioresp
# # from entidades import e_usuarioapp,e_usuarioappresp
# from .routers import api_usuarios,api_usuariosapp

# # Cabecera estándar
# libreria_path = config('PO_libreria')
# if libreria_path not in sys.path:
#     sys.path.append(libreria_path)
# from varios import *
# # Traigo variables de entorno que igual deberé importar arriba en cada .py:
# v_pathserver = os.getenv('PATHSERVER')
# v_llave = config('PO_')

# # Creo conexión
# dao = DAO()
# connection = dao.connection


# # Creo app
# app = FastAPI()
# app.include_router(api_usuarios.router)
# app.include_router(api_usuariosapp.router)
# #endregion

# #******************************************************************
# # #region API DE USUARIOS SIGMA
# # @app.get("/users")
# # async def users():              #name function thats no matter
# #     try:
# #         c_usuarios = d_listarusuarios(connection)
# #         return {"datos": c_usuarios}
# #     except Exception as ex:
# #         print("Error al consultar usuarios", ex)

# # # un usuario
# # @app.get("/users/{v_id}")    #cuando uso parametros por path debo tener cuidado. si creo una subpagina /userpath/ultimo por ej, ultimo lo va a intentar pasar como parametro, en ese caso debo poner esta nueva funciona arriba de la que espera parametro
# # async def users(v_id: int, response: Response):
# #     try:
# #         c_usuarios = d_unusuario(connection,v_id)
# #         if c_usuarios == None:
# #            response.status_code = 404
# #            return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #         else:    
# #             return {"datos": c_usuarios}
# #     except Exception as ex:
# #         print("Error al consultar usuario", ex)

# # # delete un usuario
# # @app.delete("/users/")
# # async def users(v_id: int,response: Response):    
# #     try:
# #         c_usuarios = d_unusuario(connection,v_id)
# #         if c_usuarios == None:
# #            response.status_code = 404
# #            return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #         else:    
# #             v_actualizo = d_eliminarusuario(connection,v_id)        
# #             if v_actualizo == False:
# #                 return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #             else:    
# #                 response.status_code = 204      # se devuelve solo este estado existoso                
# #     except Exception as ex:
# #         print("Error al dar de baja un usuario", ex)
        
# # @app.post("/users", status_code=status.HTTP_201_CREATED)
# # async def users(v_usuario: e_usuario):    
# #     try:    
# #         # Extraer los valores en el orden adecuado
# #         c_usuarios = d_unusuario(connection,v_id)
# #         if c_usuarios != None:
# #             response.status_code = 404
# #             return {"Atención": f"El usuario {v_id} ya existe"}
# #         else:    
# #             usuario_dict = v_usuario.dict()        
# #             v_parametros = [
# #                 usuario_dict["apellynom"],        
# #                 usuario_dict["clave"],
# #                 usuario_dict["cod_ofi"],
# #                 usuario_dict["fecha_alta"],   
# #                 usuario_dict["usuario"],                
# #                 usuario_dict["baja"],
# #                 usuario_dict["cod_sis4"]
# #             ]                
# #             d_insertarusuario(connection,v_parametros)        
# #             return {"message": "Usuario creado exitosamente", "usuario": v_usuario}
    
# #     except Exception as e:
# #         response.status_code = 500
# #         return {"error": str(e)}         

# # @app.put("/users/")
# # async def users(v_id: int, v_usuario: e_usuario, response: Response, response_model=e_usuarioresp):  
# #     try:
# #         c_usuarios = d_unusuario(connection, v_id)
# #         if c_usuarios is None:
# #             response.status_code = 404
# #             return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #         else:    
# #             usuario_dict = v_usuario.dict()            
# #             v_parametros = [
# #                 usuario_dict["apellynom"],        
# #                 usuario_dict["clave"],
# #                 usuario_dict["cod_ofi"],
# #                 usuario_dict["fecha_alta"],   
# #                 usuario_dict["usuario"],                
# #                 usuario_dict["baja"],
# #                 usuario_dict["cod_sis4"]
# #             ]                
                        
# #             v_actualizo = d_actualizarusuario(connection, v_parametros, v_id)        
# #             if not v_actualizo:
# #                 return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #             else:    
# #                 #response.status_code = 204 # si uso body no puedo mandar esto porque no permite respuesta
# #                 return e_usuarioresp(codigo=v_id, fecha_actu=datetime.date(datetime.now()))                                
            
# #     except Exception as e:
# #         response.status_code = 500
# #         return {"error": str(e)} 
# # #endregion
    
# # # #****************************************************************
# # #region API DE USUARIOS DE LA APP               
# # @app.get("/usersapp")
# # async def usersapp():              #name function thats no matter
# #     try:
# #         c_usuarios = d_listarusuariosapp(connection)
# #         return {"datos": c_usuarios}
# #     except Exception as ex:
# #         print("Error al consultar usuarios", ex)
        
# # # un usuario
# # @app.get("/usersapp/{v_id}")    #cuando uso parametros por path debo tener cuidado. si creo una subpagina /userpath/ultimo por ej, ultimo lo va a intentar pasar como parametro, en ese caso debo poner esta nueva funciona arriba de la que espera parametro
# # async def users(v_id: int, response: Response):
# #     try:
# #         c_usuarios = d_unusuarioapp(connection,v_id)
# #         if c_usuarios == None:
# #            response.status_code = 404
# #            connection.rollback()  # Descartar la transacción abortada
# #            return {"Atención": f"El usuario {v_id} no existe o fue dado de baja"}
# #         else:    
# #             return {"datos": c_usuarios}        
# #     except Exception as ex:
# #         connection.rollback()  # Descartar la transacción abortada        
# #         print("Error al consultar usuario", ex)        

# # @app.post("/usersapp", status_code=status.HTTP_201_CREATED)
# # async def createuser_app(v_usuarioapp: e_usuarioapp, response: Response):
# #     try:
# #         # Verifica si el usuario ya existe
# #         v_id = 0
# #         c_usuarios = d_unusuarioapp(connection, v_id)
# #         if c_usuarios is not None:
# #             response.status_code = status.HTTP_404_NOT_FOUND
# #             connection.rollback()  # Descartar la transacción abortada                    
# #             return {"Atención": f"El usuario de la app {v_id} ya existe"}
# #         else:
# #             v_key = str_to_key(v_llave) # llave para el hash
# #             usuario_dict = v_usuarioapp.dict()            
# #             v_parametros = [
# #                 usuario_dict["email"],
# #                 encripta(usuario_dict["password"],v_key) #encripto
# #             ]                                    

# #             nuevo_id = d_insertarusuarioapp(connection, v_parametros)            
# #             if nuevo_id is None:
# #                 response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
# #                 connection.rollback()  # Descartar la transacción abortada                                    
# #                 return {"Error": "Error al insertar en la base de datos"}
            
# #             # Crear la respuesta con la fecha actual
# #             usuarioresp_dict = {
# #                 "codigo": nuevo_id,
# #                 "fecha_alta": datetime.now()
# #             }
# #             return usuarioresp_dict
        
# #     except Exception as e:
# #         response.status_code = 500
# #         return {"error": str(e)}                             
# # #endregion



# #******************************************************************
# #region FUNCIONES USADAS POR LAS API
# def cerrarconexion():
#     dao.close()  # Cerrar la conexión al salir
    
# def s_buscarusuario(v_codigo: int):
#     usuario = list(filter(lambda user: user["codigo"] == v_codigo, usuarios_lista))
#     try:
#         return usuario[0] if usuario else {"error": f"No se encontró el usuario con el código {v_codigo}"}
#     except:
#         return {"error": "No se encontró el usuario"}

# #endregion
