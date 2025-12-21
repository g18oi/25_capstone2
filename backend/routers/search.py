from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import SessionLocal
from .. import models
from ..core.security import get_current_user

router = APIRouter(prefix="/search", tags=["search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def search_sitter(
    activities: Optional[str] = Query(None),
    regions: Optional[str] = Query(None),
    min_pay: Optional[int] = Query(None),
    max_pay: Optional[int] = Query(None),
    cctv_agree: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query("hourly_pay"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.SitterProfile).join(models.User)

    blocked_ids = db.query(models.Block.blocked_id).filter(
        models.Block.blocker_id == current_user.id
    ).subquery()

    query = query.filter(models.User.id.notin_(blocked_ids))

    if activities:
        for act in activities.split(","):
            query = query.filter(models.SitterProfile.activities.like(f"%{act.strip()}%"))

    if regions:
        for reg in regions.split(","):
            query = query.filter(models.SitterProfile.regions.like(f"{reg.strip()}%"))

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
            "id": s.id,
            "name": s.user.name if s.user else None,
            "activities": s.activities,
            "regions": s.regions,
            "hourly_pay": s.hourly_pay,
            "pay_periods": s.pay_periods,
            "cctv_agree": s.cctv_agree,
            "rematch_probability": s.rematch_probability
        }
        for s in sitters
    ]