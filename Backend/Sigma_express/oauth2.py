from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from entidades import e_tokendata
from decouple import config

v_secretkey = config('PO_jwt_secret')
v_algorithm = "HS256"
v_minutes = 480  # 8 horas

def create_access_token(data: dict):
    v_acodificar = data.copy()
    v_expira = datetime.now() + timedelta(minutes=v_minutes)
    v_acodificar.update({"exp": v_expira.timestamp()})
    return jwt.encode(v_acodificar, v_secretkey, algorithm=v_algorithm)

def verify_access_token(token: str, credentials_exception):
    try:
        decoded_token = jwt.decode(token, v_secretkey, algorithms=[v_algorithm])
        v_id: str = decoded_token.get("codigo")
        if v_id is None:
            raise credentials_exception
        return v_id
    except JWTError:
        raise credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)