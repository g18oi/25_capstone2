import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..core.security import get_current_user
from .. import models

router = APIRouter(prefix="/profile/image", tags=["Profile Image"])

UPLOAD_DIR = "uploads/profile_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_profile_image(
    file: UploadFile = File(..., description="돌보미 선생님 프로필 사진"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "sitter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="돌보미 선생님 계정만 프로필 사진을 등록할 수 있습니다."
        )

    allowed_extensions = {"png", "jpg", "jpeg"}
    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="허용되지 않는 파일 형식입니다. (png, jpg, jpeg만 가능)")
    
    filename = f"{current_user.id}_profile.{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 중 오류 발생: {e}")
    
    current_user.profile_image_path = file_path
    db.commit()

    return {"message": "프로필 사진 업로드 완료", "file_path": file_path}

@router.get("/me")
def get_my_profile_image(current_user=Depends(get_current_user)):
    """현재 사용자의 프로필 사진 경로를 반환합니다."""
    if not current_user.profile_image_path:
        return {
            "image_registered": False,
            "message": "등록된 프로필 사진이 없습니다."
        }
    return {
        "image_registered": True,
        "profile_image_path": current_user.profile_image_path
    }