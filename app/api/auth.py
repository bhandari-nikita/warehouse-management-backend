from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

from app.core.security import hash_password, verify_password
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash the password before storing. Plain password NEVER goes into DB.
    hashed_password = hash_password(user.password)

    # Create a new user instance
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"} 

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )
    
    valid_password = verify_password(
        user.password,  
        existing_user.password  
    )

    if not valid_password:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data = {
            "sub": existing_user.email,  #sub = subject represents who token belongs to.
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"  #Why Called “Bearer” Because: the bearer (holder) of token gets access.
    }