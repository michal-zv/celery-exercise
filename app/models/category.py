from sqlalchemy import Column, String
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

    files = relationship('File', back_populates="category", lazy=True, cascade="all, delete-orphan")