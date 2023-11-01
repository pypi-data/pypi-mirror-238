import logging
from fastapi import FastAPI
from axdocsystem.src.db import setup_db, get_uowf
from axdocsystem.src.settings import Settings
from axdocsystem.src.api.registrator import register_all
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
settings = Settings()  # type: ignore
uowf = get_uowf(settings)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    register_all(app, uowf, settings)
    await setup_db(uowf)

