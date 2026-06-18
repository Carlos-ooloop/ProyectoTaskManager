from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user_model import User
from schemas.user_schema import UserCreate,UserResponse,UserUpdate
from utils.auth import hash_password , admin_required 

router = APIRouter(prefix="/users",tags=["Users"])



@router.post("/register", response_model= UserResponse)

async def register(user:UserCreate, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="USER ALREADY EXISTS")
    
    hashed_password = hash_password(user.password)
    
    new_user = User(username = user.username,
                    email = user.email,
                    password = hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/",response_model= list[UserResponse])
async def get(db:Session = Depends(get_db)):
     users = db.query(User).all()
     return users
 
@router.get("/{id}", response_model= UserResponse)
async def get_by_id( id:int, db : Session= Depends(get_db)):
    
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    return user 

   

@router.put("/{id}", response_model= UserResponse, dependencies= [Depends(admin_required)])
async def act_user(id:int ,user_act:UserUpdate, db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    if user_act.username is not None:
        user.username = user_act.username
    if user_act.email is not None:
        user.email = user_act.email
    if user_act.password is not None:
        user.password = hash_password(user_act.password)
        
    db.commit()
    db.refresh(user)
    
    return user     
          
@router.delete("/{id}", dependencies=[Depends(admin_required)]) 
async def delete_user(id:int, db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code= 404, detail="USER NOT FOUND")
    db.delete(user)
    db.commit()
    
    return ("USER DELETED")   








