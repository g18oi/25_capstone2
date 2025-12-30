from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from datetime import datetime
from ..ml.model_load import MODEL_OBJECT
import pandas as pd
import numpy as np
from sqlalchemy import func
from ..core.security import get_current_user

router = APIRouter(prefix="/review", tags=["Review"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def determine_caregiver_group(scores: dict) -> int:
    tp = scores["time_punctuality"] 
    sm = scores["safety_management"]
    cc = scores["communication_with_child"]
    cs = scores["communication_skill"]
    
    if (sm >= 4) and (tp >= 4):
        return 1
    elif (cc >= 4) and (cs >= 4):
        return 2
    elif (tp <= 3) or (sm <= 3):
        return 3
    else:
        return 2
    
def calculate_rematch_probability(sitter_id: int, db: Session, review_scores: dict, caregiver_group: int) -> float:
    
    model = MODEL_OBJECT
    if model is None:
        return 100.0 

    current_date = datetime.utcnow().date()
    
    sitter_user = db.query(models.User).filter(models.User.id == sitter_id).first()
    if not sitter_user:
        return 100.0
        
    sitter_signup_dt = sitter_user.created_at.date() 

    all_matches = db.query(models.Match).filter(
        models.Match.sitter_id == sitter_id
    ).order_by(models.Match.created_at.desc()).all()

    if not all_matches:
        return 100.0
        
    latest_match_dt = all_matches[0].created_at.date()
    
    days_from_start = (current_date - sitter_signup_dt).days
    rematched_today = 1 if latest_match_dt == current_date else 0
    days_since_last_rematch = (current_date - latest_match_dt).days

    input_data = {
        "caregiver_group": caregiver_group,
        "time_punctuality": review_scores["time_punctuality"],
        "preparedness_activity": review_scores["preparedness_activity"],
        "communication_with_child": review_scores["communication_with_child"],
        "safety_management": review_scores["safety_management"],
        "communication_skill": review_scores["communication_skill"],
        "days_since_last_rematch": days_since_last_rematch,
        "rematched_today": rematched_today,
        "days_from_start": days_from_start
    }

    feature_cols = list(input_data.keys())
    X_new = pd.DataFrame([input_data], columns=feature_cols)

    prediction = model.predict(X_new)[0]
    predicted_probability = np.clip(prediction, 0.0, 100.0)

    return round(float(predicted_probability), 2)

@router.post("/create", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):

    match = db.query(models.Match).filter(models.Match.id == review.match_id).first()

    if not match:
        raise HTTPException(status_code=404, detail="매칭을 찾을 수 없습니다.")
    if match.status != "completed":
        raise HTTPException(status_code=400, detail="완료된 매칭에만 후기를 작성할 수 있습니다.")
    
    
    sitter = db.query(models.User).filter(models.User.id == review.sitter_id).first()
    if not sitter or sitter.role != "sitter":
        raise HTTPException(status_code=404, detail="해당 돌보미 정보를 찾을 수 없습니다.")
    
    sitter_profile = db.query(models.SitterProfile).filter(
        models.SitterProfile.user_id == sitter.id
    ).first()
    if not sitter_profile:
        raise HTTPException(status_code=404, detail="돌보미의 프로필 정보를 찾을 수 없습니다.")
    
    new_review = models.Review(
        match_id=review.match_id,
        parent_id=review.parent_id,
        sitter_id=review.sitter_id,
        comment=review.comment,
        created_at=datetime.utcnow(),
        time_punctuality=review.time_punctuality,
        preparedness_activity=review.preparedness_activity,
        communication_with_child=review.communication_with_child,
        safety_management=review.safety_management,
        communication_skill=review.communication_skill,
    )

    db.add(new_review)


    scores = {
        "time_punctuality": review.time_punctuality, 
        "preparedness_activity": review.preparedness_activity,
        "communication_with_child": review.communication_with_child, 
        "safety_management": review.safety_management,
        "communication_skill": review.communication_skill,
    }

    new_group_id = determine_caregiver_group(scores)

    sitter_profile.caregiver_group = new_group_id

    #별점 평균
    avg_scores_stmt = db.query(
        func.avg(models.Review.time_punctuality).label('avg_time_punctuality'),
        func.avg(models.Review.preparedness_activity).label('avg_preparedness_activity'),
        func.avg(models.Review.communication_with_child).label('avg_communication_with_child'),
        func.avg(models.Review.safety_management).label('avg_safety_management'),
        func.avg(models.Review.communication_skill).label('avg_communication_skill')
    ).filter(models.Review.sitter_id == sitter.id).one()
    
    avg_scores = avg_scores_stmt._asdict()

    if avg_scores:
        sitter_profile.avg_time_punctuality = round(avg_scores.get('avg_time_punctuality') or 0.0, 2)
        sitter_profile.avg_preparedness_activity = round(avg_scores.get('avg_preparedness_activity') or 0.0, 2)
        sitter_profile.avg_communication_with_child = round(avg_scores.get('avg_communication_with_child') or 0.0, 2)
        sitter_profile.avg_safety_management = round(avg_scores.get('avg_safety_management') or 0.0, 2)
        sitter_profile.avg_communication_skill = round(avg_scores.get('avg_communication_skill') or 0.0, 2)

    ##

    try:
        new_prob = calculate_rematch_probability(
            sitter_id=sitter.id, db=db, review_scores=scores,
            caregiver_group=new_group_id
        )
        sitter_profile.rematch_probability = new_prob
    except Exception as e:
        print(f"재매칭 확률 계산 실패: {e}")
        pass

    db.commit()
    db.refresh(new_review)

    return new_review

@router.get("/sitter/{sitter_id}")
def get_sitter_reviews(sitter_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.sitter_id == sitter_id).all()
    
    if not reviews:
        return {
            "message": "후기가 없습니다.",
            "reviews": []
        }
        
    review_list = [
        {
            "comment": r.comment,
            "created_at": r.created_at
        } for r in reviews
    ]
    
    return {
        "message": "후기 조회 성공",
        "reviews": review_list
    }

@router.put("/update/{review_id}", response_model=schemas.ReviewResponse)
def update_review(
    review_id: int, 
    review_data: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user) 
):
    existing_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not existing_review:
        raise HTTPException(status_code=404, detail="해당 후기를 찾을 수 없습니다.")
    
    if existing_review.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="후기 수정 권한이 없습니다. 작성자만 수정할 수 있습니다."
        )
    
    update_data = review_data.model_dump(exclude_unset=True) 
    score_keys = ["time_punctuality", "preparedness_activity", "communication_with_child", "safety_management", "communication_skill"]

    for key, value in update_data.items():
        setattr(existing_review, key, value)

    sitter_profile = db.query(models.SitterProfile).filter(
        models.SitterProfile.user_id == existing_review.sitter_id
    ).first()

    if sitter_profile and any(k in update_data for k in score_keys):
        current_scores = {
            
            "time_punctuality": existing_review.time_punctuality, 
            "preparedness_activity": existing_review.preparedness_activity,
            "communication_with_child": existing_review.communication_with_child, 
            "safety_management": existing_review.safety_management,
            "communication_skill": existing_review.communication_skill,
        }
        new_group_id = determine_caregiver_group(current_scores)
        sitter_profile.caregiver_group = new_group_id

        try:
            new_prob = calculate_rematch_probability(
                sitter_id=existing_review.sitter_id, db=db, review_scores=current_scores,
                caregiver_group=new_group_id
            )
            sitter_profile.rematch_probability = new_prob
        except Exception as e:
            print(f"재매칭 확률 계산 실패: {e}")
            pass

    db.commit()
    db.refresh(existing_review)

    return existing_review