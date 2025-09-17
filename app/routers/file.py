import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import File
from app.schemas import FileCreate, FileRead, FileUpdate
from app.crud import file, category
from uuid import UUID, uuid4
from app.config import settings

# make sure dir exists
os.makedirs(settings.upload_dir, exist_ok=True)

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/", response_model=FileRead)
async def upload_file(
    category_name: str, 
    uploaded_file: UploadFile, 
    db: Session = Depends(get_db)
  ):
    # make sure its an excel file
    if not uploaded_file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files allowed")

    # make sure category exists
    existing_category = category.get_category_by_name(db, category_name)
    if not existing_category:
        raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")
    
    # generate unique filename to avoid collisions
    # todo maybe change to id instead
    # todo delete file if create failed/create file after
    extention = os.path.splitext(uploaded_file.filename)[1]
    unique_name = f"{uuid4()}{extention}"
    file_path = os.path.join(settings.upload_dir, unique_name)

    # save file to local dir
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    file_in = FileCreate(
        filename=uploaded_file.filename,
        path=file_path, 
        category_id=existing_category.id
    )
    
    return file.create(db, file_in)

# routes for testing TO BE DELETED
@router.get("/", response_model=list[FileRead])
def list_files(db: Session = Depends(get_db)):
    return file.get_all(db)

# @router.get("/{file_id}", response_model=FileRead)
# def read_file_by_id(file_id: UUID, db: Session = Depends(get_db)):
#     return file.get(db, file_id)

# @router.put("/{file_id}", response_model=FileRead)
# def update_file(file_id: UUID, file_in: FileUpdate, db: Session = Depends(get_db)):
#     existing = file.get(db, file_id)
#     return file.update(db, existing, file_in)

@router.delete("/{file_id}", response_model=FileRead)
def delete_file(file_id: UUID, db: Session = Depends(get_db)):
    existing = file.get(db, file_id)
    return file.delete(db, file_id)
