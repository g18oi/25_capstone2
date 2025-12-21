from sqlalchemy.orm import Session
from .. import models
from ..core.security import get_password_hash
from datetime import datetime

def create_user(db: Session, name: str, email: str, password: str, role: str):
    hasshed_pw = get_password_hash(password)
    new_user = models.User(
        name=name,
        email=email,
        password=hasshed_pw,
        role=role,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    
    return new_user

def get_user(db:Session, name:str):
    return db.query(models.User).filter(models.User.name == name).first()

