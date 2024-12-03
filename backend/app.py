from fastapi import FastAPI
from backend.api import account,auth,appointments
from fastapi.middleware.cors import CORSMiddleware
from backend.database.database_config import engine, database, Base

app = FastAPI()
app.include_router(account.router, prefix='/app')
app.include_router(auth.router, prefix='/app')
app.include_router(appointments.router, prefix='/app')
origins = [
    "http://localhost:5173",
]

methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
#