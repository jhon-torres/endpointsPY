from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

# python -m uvicorn main:app --reload

@app.get("/")
async def root():
    return "Hola Faaast!"

@app.get("/name")
async def name():
    name = "Jhon"
    lastname = "Torres"
    return { "user" : name + " " + lastname }