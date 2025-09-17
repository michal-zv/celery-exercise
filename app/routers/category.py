from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.crud.category import category
from uuid import UUID

router = APIRouter(prefix="/categories", tags=["Categorys"])

@router.post("/", response_model=CategoryRead)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return category.create(db, category_in)

# for testing TO BE DELETED
@router.get("/", response_model=list[CategoryRead])
def list_categorys(db: Session = Depends(get_db)):
    return category.get_all(db)


# @router.get("/{category_id}", response_model=CategoryRead)
# def read_category_by_id(category_id: UUID, db: Session = Depends(get_db)):
#     return category.get(db, category_id)


# @router.put("/{category_id}", response_model=CategoryRead)
# def update_category(category_id: UUID, category_in: CategoryUpdate, db: Session = Depends(get_db)):
#     existing = category.get(db, category_id)
#     return category.update(db, existing, category_in)


# @router.delete("/{category_id}", response_model=CategoryRead)
# def delete_category(category_id: UUID, db: Session = Depends(get_db)):
#     existing = category.get(db, category_id)
#     return category.delete(db, category_id)
