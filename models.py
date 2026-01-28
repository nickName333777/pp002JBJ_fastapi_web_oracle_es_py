"""
SQLAlchemy Models for FastAPI Backend
Oracle DB 테이블에 매핑되는 모델들
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Sequence # 생성한 SEQ_TABLE__NO  자동삽입용

Base = declarative_base()


class Level(Base):
    """레벨 테이블"""
    __tablename__ = "LEVELS"
    
    level_no = Column("LEVEL_NO", Integer, primary_key=True)
    required_total_exp = Column("REQUIRED_TOTAL_EXP", Integer, nullable=False)
    title = Column("TITLE", String(100), nullable=False)
    
    # 관계 설정
    members = relationship("Member", back_populates="member_level")


class Member(Base):
    """회원 테이블"""
    __tablename__ = "MEMBER"
    
    #member_no = Column("MEMBER_NO", Integer, primary_key=True, autoincrement=True)
    member_no = Column("MEMBER_NO", Integer, Sequence("SEQ_MEMBER_NO"), primary_key=True, autoincrement=True)    
    member_email = Column("MEMBER_EMAIL", String(30), nullable=False, unique=True)
    member_pw = Column("MEMBER_PW", String(200))
    member_name = Column("MEMBER_NAME", String(30), nullable=False)
    member_nickname = Column("MEMBER_NICKNAME", String(30), nullable=False)
    member_tel = Column("MEMBER_TEL", String(13), nullable=False)
    member_career = Column("MEMBER_CAREER", String(50), nullable=False)
    member_subscribe = Column("MEMBER_SUBSCRIBE", String(1), default='N', nullable=False)
    member_admin = Column("MEMBER_ADMIN", String(1), default='N', nullable=False)
    profile_img = Column("PROFILE_IMG", String(300))
    member_del_fl = Column("MEMBER_DEL_FL", String(1), default='N', nullable=False)
    m_create_date = Column("M_CREATE_DATE", DateTime, default=datetime.now)
    subscription_price = Column("SUBSCRIPTION_PRICE", Integer, default=0, nullable=False)
    my_info_intro = Column("MY_INFO_INTRO", String(2000))
    my_info_git = Column("MY_INFO_GIT", String(200))
    my_info_homepage = Column("MY_INFO_HOMEPAGE", String(200))
    beans_amount = Column("BEANS_AMOUNT", Integer, default=0, nullable=False)
    current_exp = Column("CURRENT_EXP", Integer, default=0, nullable=False)
    member_level_no = Column("MEMBER_LEVEL", Integer, ForeignKey("LEVELS.LEVEL_NO"), nullable=False)
    
    # 관계 설정
    member_level = relationship("Level", back_populates="members")
    social_logins = relationship("SocialLogin", back_populates="member")
    
    # 제약조건
    __table_args__ = (
        CheckConstraint("MEMBER_SUBSCRIBE IN ('Y', 'N')", name="ck_member_subscribe"),
        CheckConstraint("MEMBER_ADMIN IN ('Y', 'N')", name="ck_member_admin"),
        CheckConstraint("MEMBER_DEL_FL IN ('Y', 'N')", name="ck_member_del_fl"),
    )


class Auth(Base):
    """이메일 인증 테이블"""
    __tablename__ = "AUTH"
    
    #auth_no = Column("AUTH_NO", Integer, primary_key=True, autoincrement=True)
    auth_no = Column("AUTH_NO", Integer, Sequence("SEQ_AUTH_NO"), primary_key=True, autoincrement=True)
    code = Column("CODE", String(100), nullable=False)
    email = Column("EMAIL", String(100), nullable=False, unique=True)
    create_at = Column("CREATE_AT", DateTime, default=datetime.now, nullable=False)
    
    
class SocialLogin(Base):
    """소셜 로그인 테이블"""
    __tablename__ = "SOCIAL_LOGIN"
    
    #social_no = Column("SOCIAL_NO", Integer, primary_key=True, autoincrement=True)
    social_no = Column("SOCIAL_NO", Integer,  Sequence("SEQ_SOCIAL_LOGIN_NO"), primary_key=True, autoincrement=True)
    provider = Column("PROVIDER", String(30), nullable=False)
    provider_id = Column("PROVIDER_ID", String(100), nullable=False)
    member_no = Column("MEMBER_NO", Integer, ForeignKey("MEMBER.MEMBER_NO"), nullable=False)
    
    # 관계 설정
    member = relationship("Member", back_populates="social_logins")
    
    # 제약조건: PROVIDER + PROVIDER_ID 복합 유니크
    __table_args__ = (
        UniqueConstraint('PROVIDER', 'PROVIDER_ID', name='UK_SOCIAL_LOGIN'),
    )    
