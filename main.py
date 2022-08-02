from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from Company import companyapis, dependencies
from Database.db_properties import Base, engine
from Routers import auth, todos, users

load_dotenv()

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router,
                   prefix="/companyapis",
                   tags=["companyapis"],
                   dependencies=[Depends(dependencies.get_token_header)],
                   responses={418: {"description": "Internal Use Only"}})
app.include_router(users.router)

Base.metadata.create_all(bind=engine)
