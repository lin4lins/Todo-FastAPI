from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from Database.db_properties import Base, engine
from Routers import auth, todos, users
from starlette.staticfiles import StaticFiles


app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)
