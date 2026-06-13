from db.database import SessionLocal
from models.user_model import User
from utils.auth import hash_password

def create_admin():
    
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin :
        admin = User(
            username = "admin",
            email = "admin@gmail.com",
            password = hash_password("1234"),
            role = "admin"
        )
        db.add(admin)
        db.commit()
        print("ADMIN CREATED")
        
    else:
        print("ADMIN ALREADY CREATED")
        
        
    db.close()    
        
    if __name__ == "__main__":
        create_admin()        