from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    address = Column(String, nullable=True)

    certificate_path  = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile_image_path = Column(String, nullable=True)

    survey = relationship("UserSurvey", back_populates="user", uselist=False)
    sitter_profile = relationship("SitterProfile", back_populates="user", uselist=False)

    def related_profile(self):
        if self.role == "parent":
            return self.survey
        elif self.role == "sitter":
            return self.sitter_profile
        return None
    
    parent_reviews = relationship(
        "Review",
        foreign_keys="Review.parent_id",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    sitter_reviews = relationship(
        "Review",
        foreign_keys="Review.sitter_id",
        back_populates="sitter",
        cascade="all, delete-orphan"
    )