from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import ExcelFile
from app.schemas import ExcelFileCreate, ExcelFileRead, ExcelFileUpdate
from app.crud.excel_file import excel_file
from uuid import UUID

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/", response_model=ExcelFileRead)
async def upload_file(
    category_name: str, 
    uploaded_file: UploadFile = File(...), 
    db: Session = Depends(get_db)
  ):
    # make sure its an excel file
    if not uploaded_file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files allowed")
    
    # read the file content
    try:
      file_bytes = await uploaded_file.read()
    except Exception as e:
      raise HTTPException(
        status_code=500,
        detail=f"Failed to read uploaded file: {str(e)}"
    )

    file_in = ExcelFileCreate(
        filename=uploaded_file.filename,
        content=file_bytes
    )
    
    try:
        excel_file.create(db, file_in, category_name)
        return JSONResponse(content={"message": f"File {uploaded_file.filename} created successfully"}, status_code=status.HTTP_200_OK)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# @router.get("/", response_model=list[ExcelFileRead])
# def list_files(db: Session = Depends(get_db)):
#     return file.get_all(db)


# @router.get("/{file_id}", response_model=ExcelFileRead)
# def read_file_by_id(file_id: UUID, db: Session = Depends(get_db)):
#     return file.get(db, file_id)


# @router.put("/{file_id}", response_model=ExcelFileRead)
# def update_file(file_id: UUID, file_in: FileUpdate, db: Session = Depends(get_db)):
#     existing = file.get(db, file_id)
#     return file.update(db, existing, file_in)


# @router.delete("/{file_id}", response_model=ExcelFileRead)
# def delete_file(file_id: UUID, db: Session = Depends(get_db)):
#     existing = file.get(db, file_id)
#     return file.delete(db, file_id)
