import logging
from fastapi import APIRouter, FastAPI
from app.logger import setup_logging
from app.routers import categories
from app.db.database import Base, engine

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
router = APIRouter(prefix='/api')

# if i had more time, instead of creating tables automatically when 
# FastAPI starts, i would add a database migration tool, like alembic,
# in order to manage db schema changes in a controlled & versioned way
Base.metadata.create_all(bind=engine)

# routes
router.include_router(categories)

app.include_router(router)