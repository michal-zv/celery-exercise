from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.schemas.file import FileRead

class CategoryBase(BaseModel):
    name: str
    region: str
    type: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    type: Optional[str] = None

class CategoryRead(CategoryBase):
    id: UUID
    files: List[FileRead] = []