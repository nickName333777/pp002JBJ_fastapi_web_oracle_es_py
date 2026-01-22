"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from member_router import router as member_router
from email_router import router as email_router
from database import engine, Base

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevLog API",
    description="개발자 커뮤니티 플랫폼 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(member_router)
app.include_router(email_router)


# 루트 경로 - index.html 서빙
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


# HTML 페이지 라우팅
@app.get("/login.html")
async def login_page():
    return FileResponse("static/login.html")


@app.get("/signup.html")
async def signup_page():
    return FileResponse("static/signup.html")


@app.get("/index.html")
async def index_page():
    return FileResponse("static/index.html")


# Health Check
@app.get("/health")
async def health_check():
    print("FastAPI works, anyway...")
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 개발 환경에서만 True
    )
