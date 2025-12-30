from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import SessionLocal
from .. import models, dependency
from ..core.security import get_current_user

router = APIRouter(prefix="/search", tags=["search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def search_sitter(
    activities: Optional[str] = Query(None),
    regions: Optional[str] = Query(None),
    min_pay: Optional[int] = Query(None),
    max_pay: Optional[int] = Query(None),
    cctv_agree: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query("hourly_pay"),
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(dependency.get_current_user_optional)
):
    query = db.query(models.SitterProfile).join(models.User)

    if current_user:
        blocked_ids = db.query(models.Block.blocked_id).filter(
            models.Block.blocker_id == current_user.id
        ).subquery()
        query = query.filter(models.User.id.notin_(blocked_ids))

    if activities:
        query = query.filter(
            (models.SitterProfile.activities.like(f"%{activities}%")) | 
            (models.SitterProfile.regions.like(f"%{activities}%"))
        )

    if regions:
        query = query.filter(models.SitterProfile.regions.like(f"%{regions}%"))

    if min_pay is not None:
        query = query.filter(models.SitterProfile.hourly_pay >= min_pay)
    if max_pay is not None:
        query = query.filter(models.SitterProfile.hourly_pay <= max_pay)

    if cctv_agree is not None:
        query = query.filter(models.SitterProfile.cctv_agree == cctv_agree)

    if sort_by == "hourly_pay":
        query = query.order_by(models.SitterProfile.hourly_pay.desc())
    elif sort_by == "name":
        query = query.order_by(models.User.name.asc())

    sitters = query.all()

    return [
        {
            "user_id": s.user_id,
            "name": s.user.name if s.user else "알 수 없음",
            "activities": s.activities,
            "regions": s.regions,
            "hourly_pay": s.hourly_pay,
            "pay_periods": s.pay_periods,
            "cctv_agree": s.cctv_agree,
            "rematch_probability": s.rematch_probability,
            "profile_image": s.user.profile_image_path if s.user else None
        }
        for s in sitters
    ]

from fastapi import HTTPException # 상단에 없다면 추가 필요

@router.get("/sitter/{user_id}")
def get_sitter_detail(user_id: int, db: Session = Depends(get_db)):

    sitter_user = db.query(models.User).filter(models.User.id == user_id, models.User.role == "sitter").first()
    if not sitter_user:
        raise HTTPException(status_code=404, detail="선생님 정보를 찾을 수 없습니다.")

    profile = db.query(models.SitterProfile).filter(models.SitterProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="프로필 정보가 없습니다.")

    return {
        "id": sitter_user.id,
        "name": sitter_user.name,
        "age": 2025 - int(sitter_user.created_at.year) + 20, 
        "gender": "여",
        "location": profile.regions,
        "oneLiner": profile.introduction[:30] + "..." if profile.introduction else "",
        "tags": profile.activities.split(", ") if profile.activities else [],
        "wage": profile.hourly_pay,
        "availableDays": profile.pay_periods,
        "cctv": profile.cctv_agree,
        "introduction": profile.introduction,
        
        "rematchProbability": profile.rematch_probability, 
        "reviewStats": {
            "avg_time_punctuality": profile.avg_time_punctuality or 0,
            "avg_preparedness_activity": profile.avg_preparedness_activity or 0,
            "avg_communication_with_child": profile.avg_communication_with_child or 0,
            "avg_safety_management": profile.avg_safety_management or 0,
            "avg_communication_skill": profile.avg_communication_skill or 0
        }
    }