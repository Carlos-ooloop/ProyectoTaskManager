from db.database import engine
from models.user_model import User

User.metadata.create_all(bind = engine)