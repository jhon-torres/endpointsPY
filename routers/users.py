from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["usersdb"],
                   responses={404: {"message":"No encontrado"}})

# python -m uvicorn users:app --reload

# entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str

users_list = [User(id=1,name="Jhon", surname="Torres", url="https://name.com"), 
              User(id=2,name="Elisa", surname="Vinueza", url="https://name.com"),
              User(id=3,name="Nicole", surname="Ramirez", url="https://name.com"),]

# busca el usuario con el id especificado
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        # raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"error":"Usuario no encontrado"}

# @app.get("/usersjson")
# async def usersjson():
#     return [{"name": "Jhon", "surname": "Torres", "url": "https://name.com"},
#             {"name": "Elisa", "surname": "Vinueza", "url": "https://name.com"}]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def userById(id: int):
    return search_user(id)

@router.get("/userquery/")
async def userById(id: int):
    return search_user(id)
    
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        # return {"error": "El usuario ya existe"}
        raise HTTPException(status_code=422, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return {"message": "El usuario agregado correctamente"}
    

@router.put("/user/")
async def user(user: User):
    found= False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error":"Usuario no actualizado"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):
    found= False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found= True
            return {"message":"Usuario eliminado"}
        
    if not found:
        return {"error":"Usuario no eliminado"}