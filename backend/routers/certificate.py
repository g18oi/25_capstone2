import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..core.security import get_current_user
from .. import models
from starlette.concurrency import run_in_threadpool
from ..dependency import get_verifier
from ..ml.document import ChildcareDocumentClassifier
from ..schemas import CertificateUploadResponse

router = APIRouter(prefix="/certificate", tags=["Certificate"])

UPLOAD_DIR = "uploads/certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_certification(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    verifier: ChildcareDocumentClassifier = Depends(get_verifier)
):
    allowed_extensions = {"png", "jpg", "jpeg", "pdf"}
    extension =  file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="허용되지 않는 파일 형식입니다.")
    
    filename = f"{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    file_content = await file.read()
    await run_in_threadpool(lambda: open(file_path, "wb").write(file_content))

    try:
        verification_result = await run_in_threadpool(
            verifier.classify_with_rules,
            file_path=file_path,
            base_threshold=0.70
        )

        is_verified = verification_result["verdict"]
        rule_score = verification_result.get("rule_score", 0.0)
        
    except Exception as e:
        print(f"문서 검증 중 오류 발생: {e}")
        is_verified = False 
        rule_score = 0.0

        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="문서 처리 중 서버 오류가 발생했습니다.")

    current_user.certificate_path = file_path
    current_user.is_verified = is_verified 
    db.commit()

    return{
        "message": "증명서 업로드 및 검증 완료", 
        "file_path": file_path, 
        "is_verified": is_verified,
        "rule_score": rule_score,
        "keyword_hits": verification_result.get("keyword_hit_count", 0)
    }

@router.get("/me")
def my_cert(current_user=Depends(get_current_user)):
    if not current_user.certificate_path:
        return {
            "certificate_registered": False,
            "message": "증명서가 등록되지 않았습니다."
        }
    return {
        "certificate_registered": True,
        "certificate_path": current_user.certificate_path,
        "is_verified": current_user.is_verified
    }