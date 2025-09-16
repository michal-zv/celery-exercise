from sqlalchemy.orm import Session
from app.models import ExcelFile
from app.schemas import ExcelFileCreate, ExcelFileUpdate
from app.crud.base import CRUDBase
from app.crud.category import CRUDCategory


class CRUDExcelFile(CRUDBase[ExcelFile, ExcelFileCreate, ExcelFileUpdate]):
    
    def create(self, db: Session, obj_in: ExcelFileCreate, category_name: str) -> ExcelFile:

        category = CRUDCategory.get_category_by_name(db, category_name)
        if not category:
            raise ValueError(f"Category '{category_name}' not found")
        
        db_file = ExcelFile(
            filename=obj_in.filename, 
            content=obj_in.content, 
            category_id=category.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)


excel_file = CRUDExcelFile(ExcelFile)