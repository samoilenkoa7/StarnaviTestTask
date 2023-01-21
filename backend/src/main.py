from fastapi import FastAPI

from src.api import router
from src.middlewares.middlewares import CustomMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(CustomMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
