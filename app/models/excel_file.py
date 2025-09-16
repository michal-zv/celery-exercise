from sqlalchemy import Column, LargeBinary, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class ExcelFile(Base):
    __tablename__ = "excel_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False, index=True)
    category = relationship("Category", back_populates="excel_files")