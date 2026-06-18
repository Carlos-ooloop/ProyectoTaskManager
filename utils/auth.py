from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.user_model import User
from models.refreshtoken_model import RefreshTokenRequest
from schemas.user_schema import UserResponse
from app.core.loggin import auth_logger

router = APIRouter()
SECRET = "c58c87349fe778beecdd92f9cd3467d1cf0fb829b747dac15787cc44d61e3298"
ALGORITHM = "HS256"
TOKEN_DURATION = 30

oauth = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


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
    
    if not verify_password(form.password,user.password):
        raise HTTPException(status_code=401,detail="CONTRASEÑA INCORRECTA")    
    
    acces_token = create_access_token({"sub":user.username,"role":user.role})
    refresh_token = create_refresh_token({"sub":user.username})
    
    return {"ACCESS_TOKEN": acces_token, "REFRESH_TOKEN": refresh_token, "TOKEN_TYPE":"BEARER"}




@router.post("/login/auth")
async def auth_user(token:str = Depends(oauth), db:Session=Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401,detail="TO GET ACCESS TO THIS RESOURCES YOU MUST BE AUTENTIFIED")
    try:
     username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
     if username == None:
        raise HTTPException(status_code=401,detail="THIS CREDENTIALS HAS NO VALUE")
    except JWTError:
        raise HTTPException(status_code=401,detail="THIS CREDENTIALS HAS NO VALUE")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    
    auth_logger.info(f"AUTH SUCCESS - USER_ID = {user.id}")
       
    return user
    
    
    
@router.get("/me", response_model= UserResponse)
async def me(user_auth:User = Depends(auth_user)):
    return user_auth


async def admin_required(current_user:User = Depends(auth_user)):
 if current_user.role != "admin":
        auth_logger.warning(f"USER {current_user.username} HAS NO PERMISSIONS")   
        raise HTTPException(status_code=403, detail="YOU NEDD ADMIN PERMISSION TO ACCESS TO THIS RESOURCES")
 return current_user

@router.post("/refresh")
async def refres_token(refresh_token:RefreshTokenRequest, db:Session = Depends(get_db)):
    try:
        refreshtoken = jwt.decode(refresh_token.refresh_token,SECRET,algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401,detail="INVALID REFRESH TOKEN")
    
    username = refreshtoken.get("sub")
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(status_code= 401,detail="USER NOT FOUND") 
    
    expiracion = datetime.utcnow()+timedelta(minutes= TOKEN_DURATION)    
    new_access_token = {"sub":user.username , "exp": expiracion}
    return { "ACCESS_TOKEN": jwt.encode(new_access_token,SECRET,algorithm=ALGORITHM),"TOKEN_TYPE":"BEARER"}


@router.put("/make-admin/{id}")
async def make_admin(id:int,current_user:User = Depends(admin_required), db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == id).first() 
    
    if not user:
        raise HTTPException(status_code= 404, detail="USER NOT FOUND")
    
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="USER IS ALREADY ADMIN")
    
    auth_logger.info(f"USER : {user.username} NOW IS AN ADMIN")
    user.role = "admin"
    db.commit()
    db.refresh(user)
    
    return {"INFO":f"{user.username} NOW IS AN ADMIN",
            "PROMOTED_BY":current_user.username}
    
    
@router.put("/remove-admin/{id}")
async def remove_admin(current_user:User = Depends(admin_required), db:Session=Depends(get_db)):
    
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    if user.role == "user":
        raise HTTPException(status_code=400, detail="USER IS NOT AN ADMIN ")
    if current_user.id == user.id:
        raise HTTPException(status_code=400,detail="YOU CANNOT REMOVE YOUR OWN ADMIN ROLE")
    
    auth_logger.info(f"USER {user.username} IS NO LONGER AN ADMIN")
    user.role = "user"
    db.commit()
    db.refresh(user)
    
    return {"INFO":f"{user.username} IS NO LONGER AN ADMIN",
            "REMOVED_BY":current_user.username}
    
    
    
    








