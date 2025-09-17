from sqlalchemy.orm import Session
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    
    def get_category_by_name(self, db: Session, name: str) -> Category | None:
        return db.query(Category).filter(Category.name == name).first()

category = CRUDCategory(Category)