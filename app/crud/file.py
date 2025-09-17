from sqlalchemy.orm import Session
from app.models import File
from app.schemas import FileCreate, FileUpdate
from app.crud.base import CRUDBase

class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    
    def create(self, db: Session, obj_in: FileCreate) -> File:
        db_file = File(
            filename=obj_in.filename, 
            path=obj_in.path, 
            category_id=obj_in.category_id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file


file = CRUDFile(File)