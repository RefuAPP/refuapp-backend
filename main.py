from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette import status

import models
from models.admins import Admins
from models.database import engine
from models.database import engine, db_dependency
from models.supervisors import Supervisors
from models.users import Users

from populate import create_admins, create_supervisors
from routers import auth, users, refuges, reservation
from services.auth import (
    get_user_id_from_token,
    get_admin_id_from_token,
    get_supervisor_id_from_token,
)
from services.user import (
    get_user_from_id,
    get_admin_from_id,
    get_supervisor_from_id,
)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(refuges.router)
app.include_router(reservation.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(engine)
create_admins()
create_supervisors()


@app.get("/user", status_code=status.HTTP_200_OK)
async def user(user_id: get_user_id_from_token, db: db_dependency):
    if user_id is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    current_user: Optional[Users] = get_user_from_id(user_id, db)
    return {"User": current_user}


@app.get("/admin", status_code=status.HTTP_200_OK)
async def admin(admin_id: get_admin_id_from_token, db: db_dependency):
    if admin_id is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    current_admin: Optional[Admins] = get_admin_from_id(admin_id, db)
    return {"Admin": current_admin}


@app.get("/supervisor", status_code=status.HTTP_200_OK)
async def supervisor(
    supervisor_id: get_supervisor_id_from_token, db: db_dependency
):
    if supervisor_id is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    current_supervisor: Optional[Supervisors] = get_supervisor_from_id(
        supervisor_id, db
    )
    return {"Supervisor": current_supervisor}
