from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.file import FileRead

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    region: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    type: str = Field(min_length=1, max_length=255, strip_whitespace=True)

    class Config:
        validate_by_name = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    type: Optional[str] = None

class CategoryRead(CategoryBase):
    id: UUID
    files: List[FileRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True