from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base


class UserSurvey(Base):
    __tablename__ = "user_surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)

    hope_regions = Column(String, nullable=True)
    region_detail = Column(String, nullable=True)
    hope_pay = Column(Integer, nullable=True)
    activities = Column(String, nullable=True)
    warning = Column(String, nullable=True) 
    info_agree = Column(Boolean, nullable=True)

    user = relationship("User", back_populates="survey")

    children = relationship("Child", back_populates="survey", cascade="all, delete-orphan") 
    
class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("user_surveys.id", ondelete="CASCADE"))

    child_year = Column(String, nullable=True)
    child_age = Column(Integer, nullable=True)
    child_gender = Column(String, nullable=True)

    survey = relationship("UserSurvey", back_populates="children")

class SitterProfile(Base):
    __tablename__ = "sitter_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    
    career = Column(String, nullable=True)
    career_detail = Column(String, nullable=True)
    certifications = Column(String, nullable=True)
    
    activities = Column(String, nullable=True)
    regions = Column(String, nullable=True)
    hourly_pay = Column(Integer, nullable=True)
    pay_periods = Column(String, nullable=True)
    cctv_agree = Column(Boolean, nullable=True)
    introduction = Column(String, nullable=True)
    info_agree = Column(Boolean, nullable=True)

    caregiver_group = Column(Integer, default=1)
    rematch_probability = Column(Float, default=100.0) 

    avg_time_punctuality = Column(Float, default=0.0)
    avg_preparedness_activity = Column(Float, default=0.0)
    avg_communication_with_child = Column(Float, default=0.0)
    avg_safety_management = Column(Float, default=0.0)
    avg_communication_skill = Column(Float, default=0.0)

    user = relationship("User", back_populates="sitter_profile")