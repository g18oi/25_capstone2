from sqlalchemy import Column, Integer, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from..database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"))
    parent_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    sitter_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    time_punctuality = Column(Integer, nullable=True)
    preparedness_activity = Column(Integer, nullable=True)
    communication_with_child = Column(Integer, nullable=True)
    safety_management = Column(Integer, nullable=True)
    communication_skill = Column(Integer, nullable=True)

    match = relationship("Match", back_populates="review")

    parent = relationship("User", foreign_keys=[parent_id], back_populates="parent_reviews")
    sitter = relationship("User", foreign_keys=[sitter_id], back_populates="sitter_reviews")