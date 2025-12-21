from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    sitter_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("User", foreign_keys=[parent_id])
    sitter = relationship("User", foreign_keys=[sitter_id])

    review = relationship("Review", back_populates="match", uselist=False)