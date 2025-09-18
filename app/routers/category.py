from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.crud.category import category
from uuid import UUID
from app.utils.excel import file_sum_numbers, file_contains_term

router = APIRouter(prefix="/categories", tags=["Categorys"])

@router.post("/", response_model=CategoryRead)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return category.create(db, category_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")

@router.get("/types/{type}/sum")
def sum_type(type: str, db: Session = Depends(get_db)):
    category_list = category.get_categories_by_type(db, type)
    if not category_list:
        raise HTTPException(status_code=404, detail=f"No categories found for type '{type}'")
    
    file_list = [file for cat in category_list for file in cat.files]

    summary = sum(file_sum_numbers(file.path) for file in file_list)
    return summary

@router.get("/regions/search/{search_term}")
def find_regions(search_term: str, db: Session = Depends(get_db)):
    category_list = category.get_all(db)

    # group files by region
    region_files = defaultdict(list)
    for cat in category_list:
        for file in cat.files:
            region_files[cat.region].append(file)

    matching_regions = set()
    for region, files in region_files.items():
        if any(file_contains_term(f.path, search_term) for f in files):
            matching_regions.add(region)
    
    return {"regions": list(matching_regions)}


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

@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    return category.delete(db, category_id)
