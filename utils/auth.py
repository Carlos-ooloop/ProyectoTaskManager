from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User

router = APIRouter()
SECRET = "c58c87349fe778beecdd92f9cd3467d1cf0fb829b747dac15787cc44d61e3298"
ALGORITHM = "HS256"
TOKEN_DURATION = 30

oauth = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    encriptado = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_DURATION)
    encriptado.update({"exp":expire})
    return jwt.encode(encriptado,SECRET,algorithm=ALGORITHM)


def create_refresh_token(data:dict):
    encriptado = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    encriptado.update({"exp":expire})
    return jwt.encode(encriptado,SECRET,algorithm=ALGORITHM)

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    
    user = db.query(User).filter(User.username == form.username).first()
    
    if not user:
        raise HTTPException(status_code=404,detail="USER NOT FOUND")
    
    if not verify_password(user.password,form.password):
        raise HTTPException(status_code=401,detail="CONTRASEÑA INCORRECTA")
    
    acces_token = create_access_token({"sub":user.username,"role":user.role})
    refresh_token = create_refresh_token({"sub":user.username})
    
    return {"ACCESS_TOKEN": acces_token, "REFRESH_TOKEN": refresh_token, "TOKEN_TYPE":"BEARER"}


    
    
    








