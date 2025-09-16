from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ExcelFileBase(BaseModel):
    filename: str
    content: bytes

class ExcelFileCreate(ExcelFileBase):
    category_id: UUID

class ExcelFileUpdate(BaseModel):
    filename: Optional[str] = None
    content: Optional[bytes] = None

class ExcelFileRead(ExcelFileBase):
    id: UUID
    category_id: UUID
