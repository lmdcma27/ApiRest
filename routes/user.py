from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet


key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get('/users', response_model = list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall( )

@user.post('/users', response_model = User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    conn.execute(users.insert().values(new_user))
    

@user.get('/users/{id}', response_model = User, tags=["users"])
def obtener(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return "deleted"

@user.put('/update/{id}')
def update_user(id: str, user:User):
    conn.execute(users.update().values(
        name=user.name,
        password=f.encrypt(user.password.encode("utf-8") )).where(users.c.id==id))
    return "updated"