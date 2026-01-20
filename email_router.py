"""
이메일 인증 관련 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from database import get_db
from models import Auth
from schemas import EmailAuthRequest, EmailAuthCheckRequest
from auth import generate_auth_code

router = APIRouter(prefix="/sendEmail", tags=["email"])

# 이메일 설정 (환경변수로 관리)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")


def send_email(to_email: str, subject: str, html_content: str):
    """이메일 발송"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False


@router.get("/signup")
async def send_signup_auth_email(
    email: str,
    db: Session = Depends(get_db)
):
    """회원가입 인증 이메일 발송"""
    # 인증 코드 생성
    auth_code = generate_auth_code()
    
    # 기존 인증 정보 확인
    existing_auth = db.query(Auth).filter(Auth.email == email).first()
    
    if existing_auth:
        # 기존 코드 업데이트
        existing_auth.code = auth_code
        existing_auth.create_at = datetime.now()
    else:
        # 새 인증 정보 생성
        new_auth = Auth(
            code=auth_code,
            email=email,
            create_at=datetime.now()
        )
        db.add(new_auth)
    
    db.commit()
    
    # 이메일 발송
    subject = "[DevLog Project] 회원 가입 인증코드"
    html_content = f"""
    <html>
        <body>
            <p>DevLog Project 회원 가입 인증코드입니다.</p>
            <h3 style='color:blue'>{auth_code}</h3>
        </body>
    </html>
    """
    
    email_sent = send_email(email, subject, html_content)
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="이메일 발송에 실패했습니다"
        )
    
    return {"result": 1, "message": "인증번호가 발송되었습니다"}


@router.get("/checkAuthKey")
async def check_auth_key(
    inputKey: str,
    email: str,
    db: Session = Depends(get_db)
):
    """인증 코드 확인"""
    auth = db.query(Auth).filter(
        Auth.email == email,
        Auth.code == inputKey
    ).first()
    
    if auth:
        # 인증 성공 시 해당 레코드 삭제 (재사용 방지)
        db.delete(auth)
        db.commit()
        return {"result": 1, "message": "인증되었습니다"}
    else:
        return {"result": 0, "message": "인증번호가 일치하지 않습니다"}


@router.post("/checkCode/adminCode")
async def check_admin_code(admin_code: str):
    """관리자 승인 코드 확인"""
    # 실제로는 DB에서 관리하는 것이 좋음
    ADMIN_CODE = "devlog1234"
    
    if admin_code == ADMIN_CODE:
        return {"result": 1, "message": "승인된 코드입니다"}
    else:
        return {"result": 0, "message": "승인되지 않은 코드입니다"}
