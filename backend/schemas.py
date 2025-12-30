from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import FieldValidationInfo
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from typing import Optional

#회원가입
class ChildProfile(BaseModel):
    child_year: str 
    child_age: int 
    child_gender: str
    
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password1:str
    password2:str
    role:str
    address: str | None = None

    warning: str | None = None

    children_profiles: List[ChildProfile] | None = None

    activities: List[str] | None = None     
    hope_regions: List[str] | None = None
    region_detail: str | None = None
        
    hope_pay: int | None = None 
    pay_period: List[str] | None = None      
    cctv_agree: bool | None = None
    info_agree: bool | None = None
    
    career: str | None = None
    career_detail: str | None = None
    certifications: List[str] | None = None
    introduction: str | None = None

    @field_validator('name', 'email', 'password1', 'password2')
    def not_empty(cls, v, info: FieldValidationInfo):
        if not isinstance(v, str) or not v.strip():
            raise ValueError('빈칸을 채워주세요.')
        return v
    
    @field_validator('password2')
    @classmethod
    def passwords_match(cls, v:str, info:FieldValidationInfo):
        password1 = info.data.get("password1")
        if password1 and v != password1:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v

#문서 업로드 및 검증
class CertificateUploadResponse(BaseModel):
    message: str = Field(..., description="응답 메시지")
    file_path: str = Field(..., description="서버에 저장된 파일 경로")
    is_verified: bool = Field(..., description="문서 검증 결과 (True/False)")
    rule_score: float = Field(..., description="최종 규칙 기반 유사도 점수")

    class Config:
        from_attributes = True

#로그인 
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str | None = None
    user_id: int | None = None
    name: str

class TokenData(BaseModel):
    email:str | None = None

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str
    rematch_probability: float | None = None

    class Config:
        from_attributes = True

#개인 정보 수정
class UserUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

#설문 정보 수정
class ParentSurveyUpdate(BaseModel):
    warning: Optional[str] = None

    activities: Optional[List[str]] = None      
    hope_regions: Optional[List[str]] = None    
    hope_pay: Optional[int] = None 
    info_agree: Optional[bool] = None

    children_profiles: Optional[List[ChildProfile]] = None

class SitterProfileUpdate(BaseModel):
    career: Optional[str] = None
    career_detail: Optional[str] = None
    certifications: Optional[List[str]] = None
    introduction: Optional[str] = None

    activities: Optional[List[str]] = None
    regions: Optional[List[str]] = None 
    hourly_pay: Optional[int] = None
    pay_period: Optional[List[str]] = None
    cctv_agree: Optional[bool] = None
    info_agree: Optional[bool] = None

#리뷰
class ReviewCreate(BaseModel):
    match_id: int
    parent_id: int
    sitter_id: int
    comment: str | None = None

    time_punctuality: float = Field(..., ge=1.0, le=5.0)
    preparedness_activity: float = Field(..., ge=1.0, le=5.0)
    communication_with_child: float = Field(..., ge=1.0, le=5.0)
    safety_management: float = Field(..., ge=1.0, le=5.0)
    communication_skill: float = Field(..., ge=1.0, le=5.0)

class ReviewResponse(BaseModel):
    id: int
    match_id: int
    parent_id: int
    sitter_id: int
    comment: str | None
    created_at: datetime
    
    time_punctuality: int | None
    preparedness_activity: int | None
    communication_with_child: int | None
    safety_management: int | None
    communication_skill: int | None

    class Config:
        from_attributes = True

#후기 수정
class ReviewUpdate(BaseModel):
    comment: Optional[str] = None
    
    time_punctuality: Optional[int] = Field(None, ge=1, le=5)
    preparedness_activity: Optional[int] = Field(None, ge=1, le=5)
    communication_with_child: Optional[int] = Field(None, ge=1, le=5)
    safety_management: Optional[int] = Field(None, ge=1, le=5)
    communication_skill: Optional[int] = Field(None, ge=1, le=5)


#예측 모델 연결
class RematchPredictRequest(BaseModel):

    sitter_id: int = Field(...)

    caregiver_group: int = Field(...)
    
    time_punctuality: int
    preparedness_activity: int
    communication_with_child: int
    safety_management: int
    communication_skill: int

class RematchPredictResponse(BaseModel):
    rematch_probability: float = Field(...)

#사용자 신고 및 차단
class ReportCreate(BaseModel):
    reporter_id: int 
    reported_id: int 
    reason: str      
    details: Optional[str] = None

class ReportResponse(ReportCreate):
    id: int
    created_at: datetime
    status: str
    is_processed: bool

    class Config:
        from_attributes = True

class BlockResponse(BaseModel):
    id: int
    blocker_id: int
    blocked_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

#채팅
class SendMessage(BaseModel):
    content: str

class ChatResponse(BaseModel):
    id: int
    match_id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime

    class config:
        from_attributes = True