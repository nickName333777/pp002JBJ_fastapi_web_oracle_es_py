"""
JWT 인증 및 비밀번호 해싱 유틸리티
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt 
from fastapi import Depends, HTTPException, status

from passlib.context import CryptContext 
from fastapi.security import OAuth2PasswordBearer # for 정적렌더링
#from sqlalchemy.orm import Session

import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # for jinja2 + HTMLResponse



# 환경변수로 관리해야 할 값들
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/member/login")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """비밀번호 검증"""
#     return pwd_context.verify(plain_password, hashed_password)
#
# def get_password_hash(password: str) -> str:
#     """비밀번호 해싱"""
#     return pwd_context.hash(password)

##### bcrypt 3.2.2 의 72바이트 제한 방어 (bcrypt는 무조건 72 byte 제한필요 아니면 제한없는 argon2-cffi 해시알고리즘사용 )
MAX_BCRYPT_LEN = 72

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    return pwd_context.verify(plain_password[:MAX_BCRYPT_LEN], hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:MAX_BCRYPT_LEN])



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT 액세스 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    """JWT 토큰 디코딩"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """현재 로그인한 사용자 정보 가져오기"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    member_email: str = payload.get("sub")
    if member_email is None:
        raise credentials_exception
    
    return {"member_email": member_email, "member_no": payload.get("member_no")}


def generate_auth_code() -> str:
    """6자리 인증 코드 생성"""
    import random
    import string
    
    code = ""
    for _ in range(6):
        sel = random.randint(0, 2)
        if sel == 0:
            code += str(random.randint(0, 9))
        else:
            ch = random.choice(string.ascii_uppercase)
            if random.randint(0, 1) == 0:
                ch = ch.lower()
            code += ch
    return code
