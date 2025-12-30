from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, certificate, profile_image, match, search, reviews, user_update, report, chating
from .ml import model_load
from .ml.document import ChildcareDocumentClassifier
from . import dependency

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    dependency.state["verifier"] = ChildcareDocumentClassifier(similarity_threshold=0.70)
    print("FastAPI Lifespan: 문서 검증 모델 로딩 완료")
    yield

app = FastAPI(title="아이돌봄 매칭 서비스", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(certificate.router, prefix="/api")
app.include_router(profile_image.router, prefix="/api")
app.include_router(match.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(reviews.router, prefix="/api") 
app.include_router(user_update.router, prefix="/api")
app.include_router(report.router, prefix="/api")
app.include_router(chating.router, prefix="/chat")