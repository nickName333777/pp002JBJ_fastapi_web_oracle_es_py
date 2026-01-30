"""
FastAPI 메인 애플리케이션
Jinja2 템플릿 엔진 통합
"""
### web-framework
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

### StaticFiles/FileResponse -> 정적파일서빙
# 성능 효율적: CDN 캐싱에 적합, 서버 부하가 적음; 
# SReact/Vue로 빌드된 SPA (Single Page Application)에 적합; 이미지, CSS, JS 등 정적 리소스 서빙.
from fastapi.staticfiles import StaticFiles # 
from fastapi.responses import FileResponse  # FileResponse: 요청 시 특정 파일을 직접 반환

### StaticFiles/Jinja2Templates -> 동적 템플릿 렌더링 
# 서버 측 렌더링 (SSR): 요청 시 Jinja2 템플릿 엔진이 HTML을 동적으로 생성합니다.
# 템플릿 변수 주입: Python 코드에서 전달된 데이터를 HTML에 삽입
# 동적 생성: 매 요청마다 데이터베이스 조회 결과 등을 HTML에 반영
# 템플릿 기능: 조건문({% if %}), 반복문({% for %}), 상속({% extends %}) 등이 가능
# 상대적 느림(매번 렌더링); 사용자별 맞춤 페이지(사용자프로필byDB데이터), 실시간 데이터 업데이트 필요한 대시보드에 적합
#from fastapi.templating import Jinja2Templates #  # --> /core/templates.py에서 처리( jinja2 관련 처리 여기서)
#templates = Jinja2Templates(directory="app/templates")
#
# (두 방식을 혼용해 정적 파일은 CDN으로, 동적 페이지는 Jinja2로 처리하는 하이브리드 구조도 가능)

from fastapi import Request
from fastapi.responses import HTMLResponse


###
from pathlib import Path
import os
from dotenv import load_dotenv
# 환경 변수 로드
# .env 파일 명시적 로드 (최우선)
load_dotenv(override=True)


### web-server
import uvicorn

#from member_router import router as member_router
#from email_router import router as email_router
#from kakao_router import router as kakao_router # for 카카오 소셜로그인
#from routers import member_router, email_router, kakao_router, board_router # jinja2에서 오류

from core.templates import templates # jinja2 관련 처리 여기서

from database import engine, Base

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JoBoJu API",
    description="재생에너지 장비 관리 플랫폼 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    #allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:8880").split(","),
    allow_origins=["http://localhost:3000", "http://localhost:8880"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# 정적 파일 & 템플릿 설정
# ============================================

##### 정적 파일 서빙 BY StaticFiles/FileResponse 
app.mount("/static", StaticFiles(directory="static"), name="static")

# 업로드 파일 (사용자 업로드 이미지)
#UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/mnt/user-data/uploads")
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
if os.path.exists(UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

## Jinja2 템플릿  #### => from core.templates import templates # jinja2 관련 처리 여기서
##TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")
#TEMPLATE_DIR = os.getenv("TEMPLATE_DIR")
#templates = Jinja2Templates(directory=TEMPLATE_DIR)
#
## 템플릿 전역 함수 추가 (URL 생성용)
#def url_for(request, name: str, **path_params):
#    """템플릿에서 URL 생성"""
#    return request.url_for(name, **path_params)
#
#templates.env.globals['url_for'] = url_for


# ============================================
# 라우터 등록
# ============================================

# 기존 라우터 (API): 라우터 등록
#from routers import member_router, email_router, kakao_router, board_router # jinja2에서 오류
#from routers.member_router import router as member_router
#from routers.email_router import router as email_router
#from routers.kakao_router import router as kakao_router
#from routers.board_router import router as board_router
#
#app.include_router(member_router)
#app.include_router(email_router)
#app.include_router(kakao_router) # for 카카오 소셜로그인
#app.include_router(board_router) # # 게시판 라우터 (Jinja2 템플릿)

from routers import member_router, email_router, kakao_router, board_router # for bypass
app.include_router(member_router.router)
app.include_router(email_router.router)
app.include_router(kakao_router.router) # for 카카오 소셜로그인
app.include_router(board_router.router)

from routers import board_write_router
app.include_router(board_write_router.bcu_router) # board write, update, delete router

# ============================================
# 헬스 체크
# ============================================
# Health Check
@app.get("/health")
async def health_check():
    print("####################################FastAPI works, anyway...")
    return {"status": "healthy"}

# ============================================
# favicon.icon 로딩
# ============================================
# favicon.icon 경로 설정
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# ============================================
# 메인 페이지 (old): FileResponse 정적 서빙?
# 모두 GET 요청주소
# ============================================
# 루트 경로 - index.html 서빙
@app.get("/")
async def read_root():
    return FileResponse("static/index.html") # FileResponse: 요청 시 특정 파일을 직접 반환

# HTML 페이지 라우팅
@app.get("/login.html")
async def login_page():
    #return FileResponse("static/login.html") # 정적렌더링시
    return FileResponse("templates/auth/login.html") # working for jinja2 case

@app.get("/signup.html")
async def signup_page():
    #return FileResponse("static/signup.html") # 정적렌더링시
    return FileResponse("templates/auth/signup.html")  # working for jinja2 case

#@app.get("/signUpKakao.html")
@app.get("/signupKakao.html")
async def signup_kakao_page():
    return FileResponse("static/signupKakao.html") # 정적렌더링시
    #return FileResponse("templates/auth/signUpKakao.html")  # working for jinja2 case

@app.get("/index.html")
async def index_page():
    return FileResponse("static/index.html")


# ============================================
# 메인 페이지(임시): jinja2-HTMLResponse 동적 렌더링
# ============================================

# from fastapi import Request
# from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root(request: Request): # inja2는 반드시 request를 넘겨야 함
    """메인 페이지"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "JoBoJu Community"
    })

# ============================================
# 앱 시작
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        # port=8000,
        port=8880,
        reload=True  # 개발 환경에서만 True
    )
