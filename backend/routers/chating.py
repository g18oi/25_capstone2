# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, HTTPException, Query
# from sqlalchemy.orm import Session
# from datetime import datetime 
# from jose import JWTError, jwt
# from ..database import SessionLocal
# from .. import models, schemas
# from ..core.security import SECRET_KEY, ALGORITHM
# from typing import Dict, List

# router = APIRouter(prefix="/chat", tags=["Chat"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class ConnectionnManager:
#     def __init__(self):
#         self.rooms: Dict[int, Dict[int, WebSocket]] = {}

#     async def connect(self, match_id: int, user_id: int, websocket: WebSocket):
#         await websocket.accept()
#         if match_id not in self.rooms:
#             self.rooms[match_id] = {}
#         self.rooms[match_id][user_id]  = websocket

#     def disconnect(self, match_id: int, user_id:  int):
#         if match_id in self.rooms:
#             self.rooms[match_id].pop(user_id, None)
#             if not self.rooms[match_id]:
#                 self.rooms.pop(match_id)

#     async def broadcast(self, match_id: int, message: dict):
#         if match_id in self.rooms:
#             for connection in self.rooms[match_id].values():
#                 await connection.send_json(message)

# manager = ConnectionnManager()

# @router.websocket("/ws/{match_id}/{user_id}")
# async def chat(
#     websocket: WebSocket, 
#     match_id: int, 
#     user_id: int,
#     token: str = Query(None)
#     ):

#     db = SessionLocal()

#     if token is None:
#         print("DEBUG: 토큰이 없습니다.")
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#         return

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         token_email = payload.get("sub")
        
#         if token_email is None:
#             print("DEBUG: 토큰에 이메일 정보가 없습니다.")
#             await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#             return

#         print(f"DEBUG: 인증 성공! 사용자: {token_email}")

#     except JWTError as e:
#         print(f"DEBUG: 토큰 검증 실패 (키 불일치 등): {e}")
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#         return
#     await websocket.accept()
   
#     try:

#         match = db.query(models.Match).filter(models.Match.id == match_id).first()
#         if not match or match.status not in ["pending", "accepted", "completed"] or user_id not in [match.parent_id, match.sitter_id]:
#             await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#             return

#         await manager.connect(match_id, user_id, websocket)

#         while True:
#             data = await websocket.receive_json()
#             message_data = schemas.SendMessage(**data)
            
#             receiver_id = match.sitter_id if user_id == match.parent_id else match.parent_id
#             new_msg = models.Chat(
#                 match_id=match_id, 
#                 sender_id=user_id, 
#                 receiver_id=receiver_id, 
#                 content=message_data.content
#             )
#             db.add(new_msg)
#             db.commit()

#             await manager.broadcast(match_id, {
#                 "sender_id": user_id,
#                 "content": message_data.content,
#                 "timestamp": datetime.utcnow().isoformat()
#             })
#     except WebSocketDisconnect:
#         manager.disconnect(match_id, user_id)
#     finally:
#         db.close()

# @router.get("/history/{match_id}", response_model=List[schemas.ChatResponse])
# def get_chat_history(match_id: int, db: Session = Depends(get_db)):
#     match = db.query(models.Match).filter(models.Match.id == match_id).first()
#     if not match:
#          raise HTTPException(status_code=404, detail="Match not found")
         
#     return db.query(models.Chat).filter(
#         models.Chat.match_id == match_id
#     ).order_by(models.Chat.timestamp.asc()).all()





from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime 
from jose import JWTError, jwt
from ..database import SessionLocal
from .. import models, schemas
from typing import Dict, List

router = APIRouter(prefix="", tags=["Chat"])

SECRET_KEY = "d3b4472f8f92a609c88e74d53603233e667163b14c355ba8503164e67c9f6089"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, match_id: int, user_id: int, websocket: WebSocket):
        if match_id not in self.rooms:
            self.rooms[match_id] = {}
        self.rooms[match_id][user_id] = websocket
        print(f"[DEBUG] Manager: 방 {match_id}에 유저 {user_id} 입장 완료")

    def disconnect(self, match_id: int, user_id: int):
        if match_id in self.rooms:
            self.rooms[match_id].pop(user_id, None)
            if not self.rooms[match_id]:
                self.rooms.pop(match_id)

    async def broadcast(self, match_id: int, message: dict):
        if match_id in self.rooms:
            for connection in self.rooms[match_id].values():
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

manager = ConnectionManager()

@router.websocket("/ws/{match_id}/{user_id}")
async def chat(
    websocket: WebSocket, 
    match_id: int, 
    user_id: int,
    token: str = Query(None)
    ):

    print(f"[DEBUG] 웹소켓 연결 시작 (방: {match_id}, 유저: {user_id})")

    # 1. 토큰 검증
    if token is None:
        print("[DEBUG] 실패: 토큰 없음")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_email = payload.get("sub")
        if token_email is None:
            print("[DEBUG] 실패: 토큰 이메일 없음")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        print(f"[DEBUG] 인증 성공! 이메일: {token_email}")
    except Exception as e:
        print(f"[DEBUG] 토큰 에러: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    db = SessionLocal()
    try:

        print(f"[DEBUG] DB에서 매칭 ID {match_id} 찾는 중...")
        match = db.query(models.Match).filter(models.Match.id == match_id).first()
        
        if not match:
            print(f"[DEBUG] 치명적 오류: 매칭 ID {match_id}가 DB에 없습니다!")
            print("   -> 해결책: DB 'matches' 테이블에 해당 ID가 있는지 확인하세요.")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        print(f"[DEBUG] 매칭 찾음! (부모ID: {match.parent_id}, 시터ID: {match.sitter_id})")

        if user_id != match.parent_id and user_id != match.sitter_id:
            print(f"[DEBUG] 접근 거부: 접속하려는 유저 {user_id}는 이 방의 멤버가 아닙니다.")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await manager.connect(match_id, user_id, websocket)

        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            print(f"[메시지 수신] {content}")

            receiver_id = match.sitter_id if user_id == match.parent_id else match.parent_id
            
            # DB 저장
            new_msg = models.Chat(
                match_id=match_id, 
                sender_id=user_id, 
                receiver_id=receiver_id, 
                content=content,
                timestamp=datetime.now() # timestamp 추가
            )
            db.add(new_msg)
            db.commit()

            await manager.broadcast(match_id, {
                "sender_id": user_id,
                "content": content,
                "timestamp": str(datetime.now())
            })

    except WebSocketDisconnect:
        print("[DEBUG] 유저 연결 끊김")
        manager.disconnect(match_id, user_id)
    except Exception as e:
        print(f"[DEBUG] DB 또는 로직 에러 발생: {e}")
    finally:
        db.close()

@router.get("/history/{match_id}")
def get_chat_history(match_id: int, db: Session = Depends(get_db)):
    print(f"[DEBUG] 히스토리 조회 요청: 매칭 {match_id}")
    return db.query(models.Chat).filter(
        models.Chat.match_id == match_id
    ).order_by(models.Chat.timestamp.asc()).all()