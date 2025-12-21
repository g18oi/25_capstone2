from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    reporter_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    reported_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    reason = Column(String, nullable=False) 
    details = Column(Text, nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="pending") 
    is_processed = Column(Boolean, default=False)

    reporter = relationship("User", foreign_keys=[reporter_id])
    reported = relationship("User", foreign_keys=[reported_id])