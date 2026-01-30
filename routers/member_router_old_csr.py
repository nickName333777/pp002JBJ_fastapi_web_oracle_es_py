"""
회원 관련 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, date
from typing import Dict

from database import get_db
from models import Member, Level, Auth
from schemas import (
    MemberSignUpRequest, 
    MemberLoginRequest, 
    MemberLoginResponse,
    EmailAuthRequest,
    EmailAuthCheckRequest,
    DupCheckResponse,
    LevelDTO
)
from auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    generate_auth_code,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


router = APIRouter(prefix="/member", tags=["member"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: MemberSignUpRequest,
    db: Session = Depends(get_db)
):
    """회원가입"""
    # 이메일 중복 체크
    existing_member = db.query(Member).filter(
        Member.member_email == request.member_email
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다"
        )
    
    # 기본 레벨 조회 (LV1)
    default_level = db.query(Level).filter(Level.level_no == 1).first()
    if not default_level:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="기본 레벨이 존재하지 않습니다"
        )
    
    # 새 회원 생성
    new_member = Member(
        member_email=request.member_email,
        member_pw=get_password_hash(request.member_pw),
        member_name=request.member_name,
        member_nickname=request.member_nickname,
        member_tel=request.member_tel,
        member_career=request.member_career,
        member_subscribe=request.member_subscribe or 'N',
        member_admin=request.member_admin or 'N',
        member_level_no=1,
        member_del_fl='N',
        m_create_date=datetime.now(),
        subscription_price=0,
        beans_amount=0,
        current_exp=0
    )
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return {
        "message": f"{request.member_nickname}님의 가입을 환영합니다. 로그인 후 서비스를 이용해 주세요.",
        "member_no": new_member.member_no
    }

# @router.get("/login")
# def login_page(request: Request): # 응답은 되나, 아래처럼 login.html보이도록 jinja2 템플릿 렌더링 해야함 
#    return {"msg": "login page"} 
###################    
# Jinja2 템플릿
# from core.templates import templates
# 템플릿 렌더링
# @router.get("/login") # 요청경로: "http://localhost:8880/member/login"
# def login_page(request: Request):   # 또는 login_page() of main.py에 FileResponse("templates/auth/login.html") 쓸수도있음
#                                     # => 이때 요청경로는 "http://localhost:8880/login.html" 임
#     return templates.TemplateResponse("auth/login.html", {
#         "request": request,
#         # "current_user": current_user # NameError: name 'current_user' is not defined
#     })    



@router.post("/login", response_model=MemberLoginResponse)
async def login(
    request: MemberLoginRequest,
    response: Response,
    req: Request,
    db: Session = Depends(get_db)
):
    """로그인"""
    # 회원 조회
    member = db.query(Member).filter(
        Member.member_email == request.member_email,
        Member.member_del_fl == 'N'
    ).first()
    
    if not member or not verify_password(request.member_pw, member.member_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 일치하지 않습니다"
        )
    
    # 탈퇴 회원 체크
    if member.member_del_fl == 'Y':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="탈퇴한 회원입니다"
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": member.member_email,
            "member_no": member.member_no,
            "role": "ROLE_ADMIN" if member.member_admin == 'Y' else "ROLE_USER"
        },
        expires_delta=access_token_expires
    )
    
    # 아이디 저장 쿠키 처리
    if request.save_id:
        response.set_cookie(
            key="saveId",
            value=member.member_email,
            max_age=60*60*24*30,  # 30일
            path="/"
        )
    else:
        response.delete_cookie(key="saveId", path="/")
    
    # 하루 1회 로그인 경험치 지급
    today = date.today().isoformat()
    cookie_name = f"EXP_{today}"
    exp_cookie = req.cookies.get(cookie_name, "")
    
    can_gain_exp = f"|{member.member_no}|" not in exp_cookie
    
    if can_gain_exp:
        # 경험치 증가
        member.current_exp += 50
        
        # 레벨업 체크
        new_level = db.query(Level).filter(
            Level.required_total_exp <= member.current_exp
        ).order_by(Level.level_no.desc()).first()
        
        if new_level and new_level.level_no > member.member_level_no:
            member.member_level_no = new_level.level_no
        
        db.commit()
        db.refresh(member)
        
        # 경험치 쿠키 설정
        new_cookie_value = exp_cookie + f"{member.member_no}|"
        now = datetime.now()
        next_midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        seconds_until_midnight = int((next_midnight - now).total_seconds())
        
        response.set_cookie(
            key=cookie_name,
            value=new_cookie_value,
            max_age=seconds_until_midnight,
            path="/"
        )
    
    # 레벨 정보 조회
    level = db.query(Level).filter(Level.level_no == member.member_level_no).first()
    level_dto = LevelDTO(
        level_no=level.level_no,
        title=level.title,
        required_total_exp=level.required_total_exp
    )
    
    # 응답 생성
    return MemberLoginResponse(
        member_no=member.member_no,
        member_email=member.member_email,
        member_nickname=member.member_nickname,
        role="ROLE_ADMIN" if member.member_admin == 'Y' else "ROLE_USER",
        member_admin=member.member_admin,
        member_subscribe=member.member_subscribe,
        member_del_fl=member.member_del_fl,
        member_career=member.member_career,
        profile_img=member.profile_img,
        my_info_intro=member.my_info_intro,
        my_info_git=member.my_info_git,
        my_info_homepage=member.my_info_homepage,
        subscription_price=member.subscription_price,
        beans_amount=member.beans_amount,
        current_exp=member.current_exp,
        m_create_date=member.m_create_date,
        level=level_dto,
        access_token=access_token # 유효 access_token 추가
    )


@router.get("/logout")
async def logout(response: Response):
    """로그아웃"""
    # 쿠키 삭제
    #response.delete_cookie(key="saveId", path="/") # 계속 saveId 남기려면 comment-out?
    return {"message": "로그아웃 성공"}


@router.get("/dupcheck/email", response_model=DupCheckResponse)
async def check_email_duplicate(email: str, db: Session = Depends(get_db)):
    """이메일 중복 체크"""
    exists = db.query(Member).filter(Member.member_email == email).first() is not None
    return DupCheckResponse(
        exists=exists,
        message="이미 사용 중인 이메일입니다" if exists else "사용 가능한 이메일입니다"
    )


@router.get("/dupcheck/nickname", response_model=DupCheckResponse)
async def check_nickname_duplicate(nickname: str, db: Session = Depends(get_db)):
    """닉네임 중복 체크"""
    exists = db.query(Member).filter(Member.member_nickname == nickname).first() is not None
    return DupCheckResponse(
        exists=exists,
        message="이미 사용 중인 닉네임입니다" if exists else "사용 가능한 닉네임입니다"
    )
    
    

#@router.post("/checkCode/adminCode") # DB로 관리시
@router.get("/checkCode/adminCode") # hardcode 시
async def check_admin_code(admin_code: str): #FastAPI는 파라미터 이름 엄격: admin_code ≠ adminCode
    """관리자 승인 코드 확인"""
    # 실제로는 DB에서 관리하는 것이 좋음
    ADMIN_CODE = "JoBoJu1234"
    
    if admin_code == ADMIN_CODE:
        return {"result": 1, "message": "승인된 코드입니다"}
    else:
        return {"result": 0, "message": "승인되지 않은 코드입니다"}
