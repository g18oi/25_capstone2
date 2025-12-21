from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import SessionLocal
from .. import models
from ..core.security import get_current_user

router = APIRouter(prefix="/match", tags=["Matching"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/recent/sitter")
def get_recent_sitter_matches(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user) 
):
    if current_user.role != "sitter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 기능은 돌보미 계정만 사용할 수 있습니다."
        )
    
    recent_matches = db.query(models.Match).filter(
        models.Match.sitter_id == current_user.id,
        models.Match.status.in_(["accepted", "completed"])
    ).order_by(models.Match.created_at.desc()).limit(6).all() 

    if not recent_matches:
        return {
            "message": "최근 매칭 내역이 없습니다.",
            "matches": []
        }
    
    return {
        "message": "최근 매칭 내역 조회 성공",
        "matches": [
            {
                "match_id": m.id,
                "parent_name": m.parent.name if m.parent else "탈퇴한 사용자", 
                "status": m.status,
                "created_at": m.created_at
            }
            for m in recent_matches
        ]
    }


def calculate_match_score(user_survey, sitter):
    user_activities = set(user_survey.activities) 
    sitter_activities = set(sitter.activities)
    activity_score = len(user_activities.intersection(sitter_activities)) / max(1, len(user_activities))

    user_regions = set(user_survey.hope_regions) 
    sitter_regions = set(sitter.regions) 
    region_score = len(user_regions.intersection(sitter_regions)) / max(1, len(user_regions))

    pay_score = 1 if sitter.hourly_pay >= user_survey.hope_pay else 0
    pay_period_score = 1 if user_survey.pay_period in sitter.pay_periods else 0
    cctv_score = 1 if user_survey.cctv_agree == sitter.cctv_agree else 0

    total_score = (
        0.4 * activity_score +
        0.3 * region_score +
        0.1 * pay_score +
        0.1 * pay_period_score +
        0.1 * cctv_score
    )

    return round(total_score, 3)

@router.get("/recommend/{survey_id}")
def recommend_sitters(survey_id: int, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    user_survey = db.query(models.UserSurvey).filter(models.UserSurvey.id == survey_id).first()
    if not user_survey:
        raise HTTPException(status_code=404, detail="설문지를 찾을 수 없습니다.")
    
    blocked_ids = db.query(models.Block.blocked_id).filter(
        models.Block.blocker_id == current_user.id
    ).subquery()

    sitters = db.query(models.SitterProfile).join(models.User).filter(
        models.User.id.notin_(blocked_ids)
    ).all()
    
    if not sitters:
        raise HTTPException(status_code=404, detail="추천할 수 있는 돌보미가 없습니다.")

    scored = []
    for sitter in sitters:
        score = calculate_match_score(user_survey, sitter)
        scored.append({
            "sitter_id": sitter.id,
            "name": sitter.user.name if sitter.user else None,
            "score": score
        })
    
    top_matches = sorted(scored, key=lambda x: x["score"], reverse=True)[:6]

    return {
        "survey_id": survey_id,
        "matches": top_matches
    }


@router.get("/sitter/list")
def get_sitter_match_list(
    filter_status: str = "all", 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "sitter":
        raise HTTPException(status_code=403, detail="돌보미 전용 기능입니다.")

    query = db.query(models.Match).filter(models.Match.sitter_id == current_user.id)

    if filter_status == "pending":
        query = query.filter(models.Match.status == "pending")
    elif filter_status == "confirmed":
        query = query.filter(models.Match.status.in_(["accepted", "completed"]))

    matches = query.order_by(models.Match.created_at.desc()).all()

    return [
        {
            "match_id": m.id,
            "parent_name": f"{m.parent.name} 학부모님",
            "status": m.status,
            "display_status": "수락 대기" if m.status == "pending" else "매칭 확정" if m.status == "accepted" else "거절됨",
            "date_time": m.created_at.strftime("%Y.%m.%d / %H:%M"),
            "location": m.parent.address,
            "is_pending": m.status == "pending"
        } for m in matches
    ]

@router.get("/parent/list")
def get_parent_match_list(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="학부모 전용 기능입니다.")

    matches = db.query(models.Match).filter(models.Match.parent_id == current_user.id).order_by(models.Match.created_at.desc()).all()

    result = []
    for m in matches:
        show_review_button = m.status == "completed" and m.review is None
        
        result.append({
            "match_id": m.id,
            "sitter_name": f"{m.sitter.name} 선생님과의 돌봄",
            "status_tag": "승인 대기" if m.status == "pending" else "진행중" if m.status == "accepted" else "종료됨",
            "status_description": "선생님 수락 대기 중" if m.status == "pending" else "현재 돌봄 진행 중" if m.status == "accepted" else "돌봄이 종료되었습니다",
            "date_info": m.created_at.strftime("%Y.%m.%d") + (" (예정)" if m.status == "pending" else ""),
            "show_review_button": show_review_button,
            "show_review_link": m.review is not None,
            "can_report": True
        })
    return result


@router.post("/request")
def request_match(parent_id: int, sitter_id: int, db: Session = Depends(get_db)):
    existing = db.query(models.Match).filter(
        models.Match.parent_id == parent_id,
        models.Match.sitter_id == sitter_id,
        models.Match.status.in_(["pending", "accepted"])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 매칭 요청이 존재합니다.")
    
    new_match = models.Match(parent_id=parent_id, sitter_id=sitter_id, status="pending")
    db.add(new_match)
    db.commit()
    return {"message": "매칭 요청 전송 완료", "match_id": new_match.id}

@router.post("/response")
def respond_match(match_id: int, accept: bool, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match or match.status != "pending":
        raise HTTPException(status_code=400, detail="유효하지 않은 요청입니다.")

    match.status = "accepted" if accept else "rejected"
    db.commit()
    return {"message": f"매칭이 {'수락' if accept else '거절'}되었습니다."}


@router.post("/complete/{match_id}")
def complete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match or match.status != "accepted":
        raise HTTPException(status_code=400, detail="수락된 매칭만 완료 가능합니다.")

    match.status = "completed"
    db.commit()
    return {"message": "매칭 완료", "match_id": match.id}
