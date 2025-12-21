from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..core.security import get_current_user
from typing import List

router = APIRouter(prefix="/report", tags=["Report & Block"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_data: schemas.ReportCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if report_data.reporter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="신고자는 본인이어야 합니다."
        )
    
    if report_data.reporter_id == report_data.reported_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="자기 자신을 신고할 수 없습니다."
        )
    
    reported_user = db.query(models.User).filter(models.User.id == report_data.reported_id).first()
    if not reported_user:
        raise HTTPException(status_code=404, detail="신고 대상을 찾을 수 없습니다.")
    
    existing_report = db.query(models.Report).filter(
        models.Report.reporter_id == report_data.reporter_id,
        models.Report.reported_id == report_data.reported_id,
        models.Report.is_processed == False
    ).first()

    if existing_report:
        raise HTTPException(status_code=400, detail="이미 해당 사용자에 대한 미처리 신고가 존재합니다.")

    new_report = models.Report(
        reporter_id=report_data.reporter_id,
        reported_id=report_data.reported_id,
        reason=report_data.reason,
        details=report_data.details
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    try:
        block_user_on_report(
            db=db, 
            blocker_id=new_report.reporter_id, 
            blocked_id=new_report.reported_id
        )
    except HTTPException as e:
        print(f"신고 후 자동 차단 중 오류 발생: {e.detail}")
        pass

    return new_report

def block_user_on_report(blocker_id: int, blocked_id: int, db: Session):
    
    existing_block = db.query(models.Block).filter(
        models.Block.blocker_id == blocker_id,
        models.Block.blocked_id == blocked_id
    ).first()

    if existing_block:
        raise HTTPException(status_code=400, detail="이미 차단된 사용자입니다.")

    new_block = models.Block(blocker_id=blocker_id, blocked_id=blocked_id)
    db.add(new_block)
    db.commit()
    return new_block

@router.post("/block/{blocked_id}", response_model=schemas.BlockResponse, status_code=status.HTTP_201_CREATED)
def block_user(
    blocked_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.id == blocked_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="자기 자신을 차단할 수 없습니다."
        )
    blocked_user = db.query(models.User).filter(models.User.id == blocked_id).first()
    if not blocked_user:
        raise HTTPException(status_code=404, detail="차단 대상을 찾을 수 없습니다.")

    new_block = block_user_on_report(
        blocker_id=current_user.id, 
        blocked_id=blocked_id, 
        db=db
    )
    
    db.refresh(new_block)
    return new_block

@router.delete("/unblock/{blocked_id}", status_code=status.HTTP_204_NO_CONTENT)
def unblock_user(
    blocked_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    block_entry = db.query(models.Block).filter(
        models.Block.blocker_id == current_user.id,
        models.Block.blocked_id == blocked_id
    ).first()

    if not block_entry:
        raise HTTPException(status_code=404, detail="차단 기록을 찾을 수 없습니다.")
    
    db.delete(block_entry)
    db.commit()
    return {"message": "차단이 해제되었습니다."}

@router.get("/blocks", response_model=List[schemas.BlockResponse])
def get_blocks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    blocks = db.query(models.Block).filter(
        models.Block.blocker_id == current_user.id
    ).all()
    return blocks