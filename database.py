"""
Oracle Database 연결 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
# docker-compose fastapi-backend environment에 정의되어 이미 OS에 등록된 환경 변수이므로 from dotenv import load_dotenv 필요없음
from dotenv import load_dotenv # 로컬 개발일때  + .env 사용
#load_dotenv()  # .env → OS 환경변수로 로드; 앱 시작 시 한 번만, 보통 config.py에서 처리
# .env 파일 명시적 로드 (최우선)
load_dotenv(override=True)

## 환경변수에서 DB 정보 가져오기
#DB_USER = os.getenv("DB_USER", "your_user")
#DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
#DB_HOST = os.getenv("DB_HOST", "localhost")
#DB_PORT = os.getenv("DB_PORT", "1521")
#DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")

# 환경변수에서 DB 정보 가져오기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SERVICE = os.getenv("DB_SERVICE")

# 필수 환경변수 검증
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE]):
    raise ValueError(
        "필수 환경변수가 설정되지 않았습니다. "
        f"DB_USER={DB_USER}, DB_HOST={DB_HOST}, DB_SERVICE={DB_SERVICE}"
    )

print(f"🔍 DB 연결 정보: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_SERVICE}")

# Oracle 연결 URL (Easy Connect 방식)
# cx_Oracle은 deprecated되었으므로 oracledb 사용 권장
SQLALCHEMY_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# 또는 cx_Oracle 계속 사용 시
# SQLALCHEMY_DATABASE_URL = f"oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"


# Engine 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=True  # 개발 시에만 True, 운영에서는 False
)

# SessionLocal 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """DB 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
