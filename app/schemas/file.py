from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class FileBase(BaseModel):
    filename: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    path: str = Field(min_length=1, strip_whitespace=True)

class FileCreate(FileBase):
    category_id: UUID

class FileUpdate(BaseModel):
    filename: Optional[str] = None
    path: Optional[str] = None

class FileRead(FileBase):
    id: UUID
    uploaded_at: datetime
    category_id: UUID
