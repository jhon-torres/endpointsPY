from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

# users_list = [User(id=1,name="Jhon", surname="Torres", url="https://name.com"), 
#               User(id=2,name="Elisa", surname="Vinueza", url="https://name.com"),
#               User(id=3,name="Nicole", surname="Ramirez", url="https://name.com")]

# busca el usuario con el campo especificado
def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        # raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"error":"Usuario no encontrado"}


@router.get("/usersdb", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/usersdb/{id}")
async def userById(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/userquerydb/")
async def userById(id: str):
    return search_user("_id", ObjectId(id))
    
@router.post("/usersdb/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id":id}))

    return User(**new_user)
    

@router.put("/usersdb", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:        
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"Usuario no actualizado"}

    return search_user("_id", ObjectId(user.id))

@router.delete("/usersdb/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        # print(found)
    except:
        return {"Error con la conexión"}
    
    if not found:
        return {"error":"Usuario no eliminado"}