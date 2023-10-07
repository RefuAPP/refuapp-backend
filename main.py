from fastapi import FastAPI, HTTPException
from starlette import status

import models
from models.database import engine, db_dependency
from routers import auth, users
from models.database import engine
from routers import auth, users, refuges
from services.auth import user_logged_in_dependency

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(refuges.router)

models.database.Base.metadata.create_all(engine)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_logged_in_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": user}
