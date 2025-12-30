from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
from .core.security import SECRET_KEY, ALGORITHM, get_current_user
from .ml.document import ChildcareDocumentClassifier

state = {} 

def get_verifier() -> ChildcareDocumentClassifier:
    if "verifier" not in state:
        raise RuntimeError("Document Verifier model not initialized.")
    return state["verifier"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="api/auth/token", auto_error=False)

def get_current_user_optional(
    token: str = Depends(oauth2_scheme_optional), 
    db: Session = Depends(get_db)
):
    if not token:
        return None
    try:
        from .core.security import SECRET_KEY, ALGORITHM
        from jose import jwt, JWTError
        from . import models
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return db.query(models.User).filter(models.User.email == email).first()
    except Exception:
        return None