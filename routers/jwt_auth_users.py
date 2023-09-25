from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"

# duracion en minutos 
ACCESS_TOKEN_DURATION = 1

SECRET = "2d0aa8131ec5a3989e4c393a1883ea94e905cfaab55b7501b5ce36e55b3b30c8"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "jhon":{
        "username": "jhon",
        "full_name": "Jhon Torres",
        "email": "jhon@test.test",
        "disabled": False,
        "password": "$2a$12$xXM8zTI0MbfdSwa9B3V.lefAPqXYOhOmDpTE3JYH9FscwtD.w/z06"
    },
    "jhon1":{
        "username": "jhon1",
        "full_name": "Jhon Torres1",
        "email": "jhon1@test.test",
        "disabled": True,
        "password": "$2a$12$RRTeh3EMlwNJh76gmEVyfeLseMy7Y/SB7ROCLwfH6S.aPKKK70adm"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        

    except JWTError:
        raise exception 

    return search_user(username)       

async def current_user(user: User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub":user.username, "exp":expire}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user