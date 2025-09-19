from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    region = Column(String, nullable=False)
    type = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    files = relationship('File', back_populates="category", lazy=True, cascade="all, delete-orphan")


    # created_at & updated_at are commonly added columns in db tables used to track the records
    # in this api there is no update endpoint, so updated_at won't change, 
    # but I added it if in the future the api will expand - nice to have it covered already