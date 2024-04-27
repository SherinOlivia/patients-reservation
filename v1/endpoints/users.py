from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from core.models.users import User as DBUser
from core.schemas.users import LoginResponse, LogoutResponse, RegisterResponse, UserLogin, UserRegister
from core.models.database import get_db
from sqlalchemy.orm import Session
import bcrypt, jwt, datetime, pytz

userRouter = APIRouter()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass

@userRouter.post("/register", response_model=RegisterResponse)
def register(user_data: UserRegister, db:Session = Depends(get_db)):

    try:
        existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hash_pass = hash_password(user_data.password)
        new_user = DBUser(name = user_data.name, email=user_data.email, password=hash_pass.decode('utf-8'), role=user_data.role)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Register Success",
            "data": new_user 
        }
    
    finally:
        db.close()

@userRouter.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, db:Session = Depends(get_db)):

    try:
        user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        valid_password = bcrypt.checkpw(user_data.password.encode('utf--8'), user.password.encode('utf--8'))
        if not valid_password:
            raise HTTPException(status_code=401, detail="Incorrect password")

        secret_key = "secret"

        token = jwt.encode({
            'email': user.email,
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.now(pytz.timezone('Asia/Jakarta')) + datetime.timedelta(hours=5)
        }, secret_key, algorithm='HS256')


        return {
            "message": "Login Success",
            "data": user,
            'access_token': token, 
            'token_type': 'bearer'
            }
    
    finally:
        db.close()

@userRouter.post("/logout", response_model=LogoutResponse)
def login(authorization: Optional[str] = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split()[1]
    blacklist_tokens = set()
    if token:
        blacklist_tokens.add(token)

    return {
        "message": "Logout Success"
    }

