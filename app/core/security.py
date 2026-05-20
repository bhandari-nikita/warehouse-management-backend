from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.db.dependencies import get_db
from app.models.user import User

import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

SECRET_KEY = os.getenv("SECRET_KEY")  #server uses this key to create token. Server also uses this key to verify token
ALGORITHM = os.getenv("ALGORITHM")   #→ Algorithm used to digitally sign token. HS256 is a common choice for symmetric signing, where the same secret key is used for both signing and verifying the token.

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
# Function to create JWT access token
def create_access_token(data: dict): #data contains payload information.
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    # creates actual JWT token by encoding the payload (to_encode) with the secret key and algorithm.
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise HTTPException
    
    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception
    
    return user

# Reusable authorization middleware logic
def require_role(allowed_roles: list):
    def role_checker(
            current_user = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        return current_user
    return role_checker