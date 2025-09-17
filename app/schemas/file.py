from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class FileBase(BaseModel):
    filename: str
    path: str

class FileCreate(FileBase):
    category_id: UUID
    pass

class FileUpdate(BaseModel):
    filename: Optional[str] = None
    content: Optional[bytes] = None

class FileRead(FileBase):
    id: UUID
    category_id: UUID
