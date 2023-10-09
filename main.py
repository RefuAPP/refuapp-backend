from fastapi import FastAPI, HTTPException
from starlette import status

import models
from models.database import engine
from models.database import engine
from routers import auth, users, refuges
from services.auth import user_logged_in_dependency

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(refuges.router)

models.database.Base.metadata.create_all(engine)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(current_user: user_logged_in_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": current_user}
