from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, crud
from ..database import SessionLocal
from datetime import timedelta
from ..database import SessionLocal
from ..core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime
from pydantic import BaseModel


router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user:schemas.UserCreate,  db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    new_user = crud.create_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password1,
        role=user.role,
    )
    db.flush()

    if user.role == "parent":
        survey = models.UserSurvey(
            user_id=new_user.id,
            hope_regions=", ".join(user.hope_regions) if isinstance(user.hope_regions, list) else user.hope_regions,
            region_detail=user.region_detail,
            hope_pay=user.hope_pay,
            activities=", ".join(user.activities) if isinstance(user.activities, list) else user.activities,
            warning=user.warning,
            info_agree=user.info_agree
        )
        db.add(survey)
        db.flush()

        if user.children_profiles:
            for child_data in user.children_profiles:
                new_child = models.survey.Child(
                    survey_id=survey.id,
                    child_year=child_data.child_year,
                    child_age=child_data.child_age,
                    child_gender=child_data.child_gender
                )
                db.add(new_child)

    elif user.role == "sitter":
        sitter = models.SitterProfile(
            user_id=new_user.id,
            activities=", ".join(user.activities) if isinstance(user.activities, list) else user.activities,
            regions=", ".join(user.hope_regions) if isinstance(user.hope_regions, list) else user.hope_regions,
            hourly_pay=user.hope_pay, 
            pay_periods=", ".join(user.pay_period) if isinstance(user.pay_period, list) else user.pay_period,
            cctv_agree=user.cctv_agree,
            info_agree=user.info_agree,

            career=user.career,
            career_detail=user.career_detail,
            certifications=", ".join(user.certifications) if isinstance(user.certifications, list) else user.certifications,
            introduction=user.introduction
        )
        db.add(sitter)

    db.commit()

    rematch_prob = None
    if user.role == "sitter":
        sitter_profile = db.query(models.SitterProfile).filter(models.SitterProfile.user_id == new_user.id).first()
        rematch_prob = sitter_profile.rematch_probability if sitter_profile else None

    return schemas.UserResponse(
    id=new_user.id,
    name=new_user.name,
    email=new_user.email,
    role=new_user.role,
    rematch_probability=rematch_prob
)


#회원가입때 선택한 지역과 실제 위치 비교 API
class RegionCheck(BaseModel):
    address: str
    regions: str

@router.post("/region-check") 
def check_region(data: RegionCheck):
    if not data.address or not data.regions:
        raise HTTPException(status_code=400, detail="주소 정보가 부족합니다.")

    actual_region = " ".join(data.address.split()[:2])
    selected_region = " ".join(data.regions.split()[:2])

    if actual_region != selected_region:
        return {
            "match": False,
            "message": f"현재 위치({actual_region})와 입력한 활동 지역({selected_region})이 다릅니다."
        }

    return {"match": True, "message": "현재 위치와 활동 지역이 일치합니다."}
    


@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="존재하지 않는 이메일입니다.")
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id,
        "name": user.name
        }

