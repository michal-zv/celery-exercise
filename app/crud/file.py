from sqlalchemy.orm import Session
from app.models import File
from app.schemas import FileCreate, FileUpdate
from app.crud.base import CRUDBase

class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    pass


file = CRUDFile(File)