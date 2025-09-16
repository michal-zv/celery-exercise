from fastapi import APIRouter, FastAPI
from app.routers import categories, files
from app.db.database import Base, engine

app = FastAPI()
router = APIRouter(prefix='/api')

# Create tables automatically when FastAPI starts
# todo change to alembic
Base.metadata.create_all(bind=engine)

# test
@app.get("/")
def test():
    return {"ping": "pong"}

app.include_router(router)