from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from entidades import e_tokendata
#from passlib.context import CryptContext

v_secretkey = "gustavoadriancerati"
#v_crypt = CryptContext(schemes=["bcrypt"])
v_algorithm = "HS256"
v_minutes=60

def create_access_token(data: dict):
    v_acodificar = data.copy()
    v_expira = datetime.now() + timedelta(minutes=v_minutes)
    v_acodificar.update({"exp": v_expira.timestamp()})  # Convertir a timestamp en segundos
    v_codificado = jwt.encode(v_acodificar, v_secretkey, algorithm=v_algorithm)    
    return v_codificado

def verify_access_token(token: str,credentials_exception):
    try:        
        decoded_token = jwt.decode(token, v_secretkey, algorithms=[v_algorithm])        
        v_id: str = decoded_token.get("codigo")            
        # print(decoded_token)        
        # input()    
        if v_id is None:
            raise credentials_exception       
        # token_data = e_tokendata(id=decoded_token)     
        return v_id
    
    except JWTError:
        raise credentials_exception

# esta funcion de la forma get_current_user: inte = Depends(oauth2.get_current_user) a debo pasar como parametro en cada endpoint de la api para validar que el usuario este correctamente logueado y no se haya vencido su token 7:24 del video Harvard
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
def get_current_user(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Credenciales invalidas", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)

# # Verificar el token generado
# decoded_token = verify_access_token(token)
# print(decoded_token)
