from typing import Optional

from fastapi import FastAPI, HTTPException
from starlette import status
from fastapi.staticfiles import StaticFiles

import models
from models.database import engine
from models.database import engine, db_dependency
from models.users import Users
from routers import auth, users, refuges
from services.auth import get_user_id_from_token
from services.user import get_user_from_id

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(refuges.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(engine)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user_id: get_user_id_from_token, db: db_dependency):
    if user_id is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    current_user: Optional[Users] = get_user_from_id(user_id, db)
    return {"User": current_user}
