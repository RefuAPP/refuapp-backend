from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

import models
from models.database import engine
from models.database import engine
from routers import auth, users, refuges, reservation
from routers import images

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

app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(engine)


@app.get("/")
def root():
    return RedirectResponse(url='/docs')
