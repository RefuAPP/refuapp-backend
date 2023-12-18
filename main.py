import firebase_admin  # type: ignore
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from firebase_admin import credentials  # type: ignore
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import models
from models.database import engine
from models.database import engine
from populate import (
    create_admin,
    create_default_sensor_refuge,
    create_supervisor,
)
from routers import auth, users, refuges, reservation, images, data

app = FastAPI(
    title="RefuApp API",
    description="User, refuge and reservations management API for RefuApp",
    docs_url='/docs',
    redoc_url='/redoc',
    version="0.1.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(refuges.router)
app.include_router(images.router)
app.include_router(reservation.router)
app.include_router(data.router)
app.router.redirect_slashes = False

app.mount("/static", StaticFiles(directory="static"), name="static")

firebase_cred = credentials.Certificate("firebase-admin-sdk.json")
firebase_admin.initialize_app(firebase_cred)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

models.database.Base.metadata.create_all(engine)
create_admin()
create_supervisor()
create_default_sensor_refuge()


@app.get("/")
def root():
    return RedirectResponse(url='/docs')
