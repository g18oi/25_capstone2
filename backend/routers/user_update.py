from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from .. import schemas, models
from ..database import SessionLocal
from ..core.security import get_current_user

router = APIRouter(prefix="/user", tags=["User Update"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=schemas.UserResponse)
def read_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    user_info = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }

    if current_user.role == "sitter":
        profile = db.query(models.SitterProfile).filter(models.SitterProfile.user_id == current_user.id).first()
        if profile:
            user_info.update({
                "career": profile.career,
                "career_detail": profile.career_detail,
                "certifications": profile.certifications,
                "activities": profile.activities,
                "hope_regions": profile.regions,
                "hope_pay": profile.hourly_pay,
                "pay_periods": profile.pay_periods,
                "cctv_agree": profile.cctv_agree,
                "introduction": profile.introduction,
                "rematch_probability": profile.rematch_probability
            })
            
    elif current_user.role == "parent":
        profile = db.query(models.UserSurvey).filter(models.UserSurvey.user_id == current_user.id).first()
        if profile:
            user_info.update({
                "hope_regions": profile.hope_regions,
                "hope_pay": profile.hope_pay,
                "activities": profile.activities,
                "warning": profile.warning,
                "info_agree": profile.info_agree
            })

    return user_info

@router.put("/update", response_model=schemas.UserResponse)
def update_my_profile(
    user_data: schemas.UserUpdate = Depends(), 
    parent_survey_data: schemas.ParentSurveyUpdate = Depends(), 
    sitter_profile_data: schemas.SitterProfileUpdate = Depends(), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    
    user_update_data = user_data.model_dump(exclude_unset=True) 
    
    for key, value in user_update_data.items():
        setattr(current_user, key, value)

    profile = current_user.related_profile() 
    if not profile:
        raise HTTPException(status_code=404, detail="사용자 프로필/설문 정보를 찾을 수 없습니다.")
    
    if current_user.role == "parent":
        profile_update_data = parent_survey_data.model_dump(exclude_unset=True)

        if 'children_profiles' in profile_update_data and profile_update_data['children_profiles'] is not None:
            new_children = profile_update_data.pop('children_profiles')
            profile.children.clear() 
            db.flush()

            for child_data in new_children:
                new_child = models.Child(
                    survey_id=profile.id,
                    child_year=child_data['child_year'], 
                    child_age=child_data['child_age'],
                    child_gender=child_data['child_gender']
                )
                db.add(new_child)

        for key, value in profile_update_data.items():

            if isinstance(value, list):
                value = ", ".join(value)
            setattr(profile, key, value)
            
    elif current_user.role == "sitter":
        profile_update_data = sitter_profile_data.model_dump(exclude_unset=True)

        for key, value in profile_update_data.items():
            if isinstance(value, list):
                value = ", ".join(value)
            
            if key == "pay_period":
                setattr(profile, "pay_periods", value)
            elif key == "regions": 
                setattr(profile, "regions", value)
            else:
                setattr(profile, key, value)

    db.commit()
    current_user = db.merge(current_user)
    db.refresh(current_user)
    
    rematch_prob = current_user.sitter_profile.rematch_probability if current_user.role == "sitter" and current_user.sitter_profile else None

    return schemas.UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        rematch_probability=rematch_prob
    )