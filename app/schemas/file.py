from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class FileBase(BaseModel):
    filename: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    
    class Config:
        validate_by_name = True

class FileCreate(FileBase):
    category_id: UUID

class FileUpdate(BaseModel):
    filename: Optional[str] = None
    path: Optional[str] = Field(min_length=1, strip_whitespace=True)

class FileRead(FileBase):
    id: UUID
    path: str
    category_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
