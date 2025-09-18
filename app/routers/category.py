import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import CategoryCreate, CategoryRead, FileCreate, FileRead, FileUpdate
from app.crud import category, file
from app.config import settings
from app.services.storage import LocalStorage
from app.utils.excel import file_sum_numbers, file_contains_term, validate_excel_file

router = APIRouter(prefix="/categories", tags=["Categories"])

storage = LocalStorage(settings.UPLOAD_DIR)

@router.post("/", response_model=CategoryRead)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return category.create(db, category_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")
    

@router.post("/{category_name}/upload-file", response_model=FileRead)
async def upload_file(
    category_name: str, 
    uploaded_file: UploadFile, 
    db: Session = Depends(get_db)
  ):
    # make sure its a valid excel file
    validate_excel_file(uploaded_file)

    # make sure category exists
    existing_category = category.get_category_by_name(db, category_name)
    if not existing_category:
        raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")
    
    try:
        file_in = FileCreate(
            filename=uploaded_file.filename,
            category_id=existing_category.id
        )
        db_file = file.create(db, file_in)

        # save file
        file_path = storage.save_file(uploaded_file.file, uploaded_file.filename, db_file.id)

        file_in = FileUpdate(path=file_path)
        return file.update(db, db_file, file_in)

    except Exception as e:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        if db_file:
            file.delete(db, db_file.id)

        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/types/{type}/sum")
def sum_type(type: str, db: Session = Depends(get_db)):
    category_list = category.get_categories_by_type(db, type)
    if not category_list:
        raise HTTPException(status_code=404, detail=f"No categories found for type '{type}'")
    
    summary = sum(
        file_sum_numbers(file.path)
        for cat in category_list
        for file in cat.files
    )

    return {"sum": summary}


@router.get("/regions/search/{search_term}")
def find_regions(search_term: str, db: Session = Depends(get_db)):
    category_list = category.get_all(db)

    matching_regions = set()
    for cat in category_list:
        for f in cat.files:
            if file_contains_term(f.path, search_term):
               matching_regions.add(cat.region)
               break  # stop checking files in this category once match is found
    
    return {"regions": list(matching_regions)}

