from fastapi import APIRouter, FastAPI
from app.routers import categories, files
from app.db.database import Base, engine

app = FastAPI()
router = APIRouter(prefix='/api')

# if i had more time, instead of creating tables automatically when 
# FastAPI starts, i would add a database migration tool, like alembic,
# in order to manage db schema changes in a controlled & versioned way
Base.metadata.create_all(bind=engine)

# routes
router.include_router(categories)
router.include_router(files)

app.include_router(router)