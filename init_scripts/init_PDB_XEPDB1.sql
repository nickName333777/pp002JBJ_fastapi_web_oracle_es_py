------------------------------------------------------------
-- PDB (Pluggable DB, 서비스name: XEPDB1) 용 유저 생성 by 관리자
-- [여기부터 4줄 관리자 계정접속해서 PDB(XEPDB1)에 'jbj_user'계정 생성]
------------------------------------------------------------
--
--
---- 1. 관리자 계정(sys as sysdba)으로 접속
---- 관리자 계정임을 확인
--SELECT USER FROM dual;
---- 'SYS' 나와야함
--
---- 2. CDB$ROOT로 이동 후 새 PDB (XEPDB1) 생성
---- 2-0) CDB 루트에서 실행
--ALTER SESSION SET CONTAINER = CDB$ROOT;
--SHOW CON_NAME; 
---- CDB$ROOT 나옴
--
---- CDB 레벨 확인
--SELECT 'CDB (XE)' as location, username, account_status, common 
--FROM cdb_users;
----WHERE username = 'JBJ_USER'; # 'JBJ_USER'가 CDB, PDB에 각각 하나씩 있을 수 있으나, 이름만 같을뿐 별개의 nampespace
--
---- 2-1) 모든 PDB 목록 확인
--SHOW PDBS;
--SELECT name, open_mode FROM v$pdbs;
--
---- 2-2) XEPDB1 생성 (admin 사용자 포함)
--CREATE PLUGGABLE DATABASE XEPDB1 
--ADMIN USER xepdb1_admin IDENTIFIED BY xepdb1_pass123
--ROLES=(CONNECT, RESOURCE, DBA)
--FILE_NAME_CONVERT=(
--  '/opt/oracle/oradata/XE/pdbseed/',
--  '/opt/oracle/oradata/XE/XEPDB1/'
--);
--
---- 2-3) PDB 열기
--ALTER PLUGGABLE DATABASE XEPDB1 OPEN;
--
---- 3. 새 PDB로 접속 테스트
--ALTER SESSION SET CONTAINER = XEPDB1;
--SHOW CON_NAME;  
---- "XEPDB1" 나옴
--
---- 모든 사용자 계정 조회
--SELECT username FROM dba_users;
---- 기존 사용자 삭제 (테이블 등 객체도 함께 삭제)
--DROP USER jbj_user CASCADE;
---- 기존 사용자 삭제 확인
--SELECT username FROM dba_users WHERE username = 'JBJ_USER';
---- 아무 결과도 안 나오면 성공
--
---- 새 사용자 생성
--CREATE USER jbj_user IDENTIFIED BY jbj_pass123;
----GRANT CONNECT, RESOURCE, CREATE TABLE TO jbj_user;
---- 권한 부여
--GRANT CONNECT, RESOURCE, CREATE VIEW TO jbj_user;
---- CONNECT : DB 연결 권한 ROLE (SET CONTAINER, CREATE SESSION; 2개 권한)
---- RESOURCE : DB 기본 객체 생성 권한 ROLE (CREATE INDEXTYPE, 
--                   --  CREATE OPERATOR, CREATE TYPE, CREATE TRIGGER,
--                   --  CREATE PROCEDURE, CREATE SEQUENCE, CREATE CLUSTER
--                   -- CREATE TABLE; 8개 권한)
---- 객체 생성 공간 할당성QUOTA UNLIMITED ON SYSTEM;
----ALTER USER jbj_user DEFAULT TABLESPACE SYSTEM
----QUOTA UNLIMITED ON SYSTEM;
--ALTER USER jbj_user DEFAULT TABLESPACE USERS
--                    TEMPORARY TABLESPACE TEMP
--                    QUOTA UNLIMITED ON USERS;
--
--COMMIT;
--
---- 확인
--SELECT username, account_status, common
--FROM dba_users 
--WHERE username = 'JBJ_USER';
--
---- 현재 PDB 확인
--SHOW CON_NAME;
---- XEPDB1 나옴
--
---- XEPDB1 레벨 확인
--SELECT 'PDB (XEPDB1)' as location, username, account_status, common 
--FROM dba_users;
----WHERE username = 'JBJ_USER';
--
---- 모든 PDB 목록 확인 (CDB 보다는 적은 목록확인 가능)
--SHOW PDBS;
--SELECT name, open_mode FROM v$pdbs;
--
--
------ [[[ Oracle 멀티테넌트 구조 ]]]
----CDB (Container Database: XE)
----├── PDB$SEED (템플릿)
----├── XEPDB1 (기본 PDB)
----├── XEPDB2 (새로 생성)
----├── XEPDB3 (추가 생성)
----└── ... XEPDBn
----
--
------ [[[ docker-compose.yml의 FastAPI에서 각각 독립 연결 ]]]
----# docker-compose.yml
----services:
----  fastapi-app1:
----    environment:
----      - DB_SERVICE=XEPDB1  # 1번째 앱
----      - DB_USER=myapp1_user
----
----  fastapi-app2:
----    environment:
----      - DB_SERVICE=XEPDB2  # 2번째 앱  
----      - DB_USER=myapp2_user
----
----  fastapi-app3:
----    environment:
----      - DB_SERVICE=XEPDB3  # 3번째 앱
----      - DB_USER=myapp3_user
--
------ [[[ PDB별 독립성 ]]]
----     완전 격리: 각 PDB는 독립된 스키마, 사용자, 데이터
----     공유 CDB: 백업/복구/모니터링은 CDB에서 통합 관리
----     Plug/Unplug: PDB 파일 복사로 이관 가능
----     리소스 격리: CPU/메모리/스토리지 독립 할당 가능
--
--
------ [[[ PDB 관리 명령어 ]]]
------ 모든 PDB 목록
----SHOW PDBS;
------ 특정 PDB 열기/닫기
----ALTER PLUGGABLE DATABASE XEPDB1 OPEN;
----ALTER PLUGGABLE DATABASE XEPDB1 CLOSE IMMEDIATE;
------ PDB 삭제
----DROP PLUGGABLE DATABASE XEPDB1 INCLUDING DATAFILES;
------ PDB 복제
----CREATE PLUGGABLE DATABASE XEPDB2 FROM XEPDB1;
--
--
--


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- ### 추천: 일반 작업용 연결은 PDB(XEPDB1) 사용 + 개발/관리용 연결은 SQL Developer로 관리
-- ['jbj_user'계정 젒속하여 init.sql 실행]
-------------------------------------------------------------------------------
---- SQL Developer로 XEPDB1의 사용자도 관리: 완전히 가능하고 권장
---- ## 📝 SQL Developer로 XEPDB1 접속 설정
--
--### 방법 1: 새 연결 추가 (PDB 전용)
--SQL Developer에서:
--```
--Connection Name: Oracle21c_XEPDB1
--Username: jbj_user
--Password: jbj_password1234
--Connection Type: Basic
--Hostname: localhost
--Port: 1521
--Service name: XEPDB1  ← 이게 중요!
--```
--또는
--```
--Connection Name: Oracle21c_XEPDB1_SID
--Username: jbj_user
--Password: jbj_password1234
--Connection Type: Basic
--Hostname: localhost
--Port: 1521
--SID: (체크하지 않음)
--Service name: XEPDB1
--```
--
--### 방법 2: TNS 방식
--`tnsnames.ora` 파일에 추가:
--```
--XEPDB1 =
--  (DESCRIPTION =
--    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
--    (CONNECT_DATA =
--      (SERVER = DEDICATED)
--      (SERVICE_NAME = XEPDB1)
--    )
--  )
--```
--SQL Developer 연결:
--```
--Connection Type: TNS
--Network Alias: XEPDB1
--Username: jbj_user
--Password: jbj_password1234
--```
--
--### 방법 3: Easy Connect
--SQL Developer 연결:
--```
--Connection Type: Custom JDBC
--Custom JDBC URL: jdbc:oracle:thin:@localhost:1521/XEPDB1
--Username: jbj_user
--Password: jbj_password1234
--

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- JBJ Database 초기화 스크립트




--DROP TABLE VIEW_LOG; -- MEMBER, BOARD, LEVELS
--DROP TABLE "USER_BEN";
--DROP TABLE "COFFEE_BEANS_HISTORY";
--DROP TABLE "MESSAGE_IMG";
--DROP TABLE "RECOMMEND_BOOKS";
--DROP TABLE "BLOG_TAG";
--DROP TABLE "COFFEE_BEANS_TRADE";
--DROP TABLE "JOB_POSTING"; 
--DROP TABLE "REPORT";
--DROP TABLE "COFFEE_BEANS_EXCHANGE";
--DROP TABLE "MESSAGE_EMOJI";
--DROP TABLE "FOLLOW";
DROP TABLE "AUTH";
--DROP TABLE "COFFEE_BEANS_PAY";
--DROP TABLE "TAG";
--DROP TABLE "REPORT_CODE";
--DROP TABLE "CHATTING_USER";
--DROP TABLE "CAFE_IMAGE";
--DROP TABLE "MESSAGE";
--DROP TABLE "COMMENT_LIKE";
--DROP TABLE "VISIT_COUNT";
DROP TABLE "CB_TOKEN_USAGE";
--DROP TABLE "USER_SCRAP";
DROP TABLE "SOCIAL_LOGIN";
DROP TABLE "NOTIFICATION";
DROP TABLE "BOARD_IMG";
DROP TABLE "CB_SESSION";
--DROP TABLE "SUBSCRIBE";
DROP TABLE "BOARD_LIKE";
--DROP TABLE "BANK_INFO";
--DROP TABLE "CAFE_REVIEW_KEYWORD";
--DROP TABLE "COMPANY_CODE";
--DROP TABLE "RECOMMEND_CAFES";
DROP TABLE "COMMENT";
--DROP TABLE "BLOG";
--DROP TABLE "EMOJI";
DROP TABLE "BOARD";
--DROP TABLE "CHATTING_ROOM";
DROP TABLE "MEMBER";
DROP TABLE "LEVELS";
DROP TABLE "BOARDTYPE";





-- LEVELS 테이블 생성
DROP TABLE "LEVELS";
CREATE TABLE LEVELS (
    LEVEL_NO NUMBER NOT NULL,
    REQUIRED_TOTAL_EXP NUMBER NOT NULL,
    TITLE VARCHAR2(100) NOT NULL,
    CONSTRAINT PK_LEVELS PRIMARY KEY (LEVEL_NO)
);

COMMENT ON COLUMN LEVELS.LEVEL_NO IS 'LV1 ~ LV30';
COMMENT ON COLUMN LEVELS.REQUIRED_TOTAL_EXP IS '레벨별 필요 누적 경험치';
COMMENT ON COLUMN LEVELS.TITLE IS '레벨별 타이틀';

--SELECT * FROM "LEVELS";
--SELECT SEQ_LEVEL_NO.NEXTVAL from dual; -- 시퀀스없으면 에러: ORA-02289: sequence does not exist
--DELETE FROM "LEVELS"; 
--DROP SEQUENCE SEQ_LEVEL_NO; 
-- 시퀀스 생성
--CREATE SEQUENCE SEQ_LEVEL_NO START WITH 1 NOCACHE;

-- MEMBER 테이블 생성
CREATE TABLE MEMBER (
    MEMBER_NO NUMBER NOT NULL,
    MEMBER_EMAIL VARCHAR2(30) NOT NULL,
    MEMBER_PW VARCHAR2(200),
    MEMBER_NAME VARCHAR2(30) NOT NULL,
    MEMBER_NICKNAME VARCHAR2(30) NOT NULL,
    MEMBER_TEL VARCHAR2(13) NOT NULL,
    MEMBER_CAREER VARCHAR2(50) NOT NULL,
    MEMBER_SUBSCRIBE CHAR(1) DEFAULT 'N' NOT NULL,
    MEMBER_ADMIN CHAR(1) DEFAULT 'N' NOT NULL,
    PROFILE_IMG VARCHAR2(300),
    MEMBER_DEL_FL CHAR(1) DEFAULT 'N' NOT NULL,
    M_CREATE_DATE DATE DEFAULT SYSDATE,
    SUBSCRIPTION_PRICE NUMBER DEFAULT 0 NOT NULL,
    MY_INFO_INTRO VARCHAR2(2000),
    MY_INFO_GIT VARCHAR2(200),
    MY_INFO_HOMEPAGE VARCHAR2(200),
    BEANS_AMOUNT NUMBER DEFAULT 0 NOT NULL,
    CURRENT_EXP NUMBER DEFAULT 0 NOT NULL,
    MEMBER_LEVEL NUMBER NOT NULL,
    CONSTRAINT PK_MEMBER PRIMARY KEY (MEMBER_NO),
    CONSTRAINT FK_LEVELS_TO_MEMBER FOREIGN KEY (MEMBER_LEVEL) REFERENCES LEVELS(LEVEL_NO),
    CONSTRAINT UK_MEMBER_EMAIL UNIQUE (MEMBER_EMAIL)
);
COMMENT ON COLUMN "MEMBER"."MEMBER_NO" IS '회원번호(SEQ_MEMBER_NO)';
COMMENT ON COLUMN "MEMBER"."MEMBER_EMAIL" IS '회원이메일(아이디)';
COMMENT ON COLUMN "MEMBER"."MEMBER_PW" IS '회원비밀번호';
COMMENT ON COLUMN "MEMBER"."MEMBER_NAME" IS '회원이름';
COMMENT ON COLUMN "MEMBER"."MEMBER_NICKNAME" IS '회원닉네임';
COMMENT ON COLUMN "MEMBER"."MEMBER_TEL" IS '회원전화번호';
COMMENT ON COLUMN "MEMBER"."MEMBER_CAREER" IS '회원경력사항';
COMMENT ON COLUMN "MEMBER"."MEMBER_SUBSCRIBE" IS '회원전용메일수신동의';
COMMENT ON COLUMN "MEMBER"."MEMBER_ADMIN" IS '관리자계정여부(Y:관리자, N:일반회원)';
COMMENT ON COLUMN "MEMBER"."PROFILE_IMG" IS '프로필 이미지';
COMMENT ON COLUMN "MEMBER"."MEMBER_DEL_FL" IS '회원탈퇴여부';
COMMENT ON COLUMN "MEMBER"."M_CREATE_DATE" IS '회원가입일';
COMMENT ON COLUMN "MEMBER"."SUBSCRIPTION_PRICE" IS '나를구독하면 지불해야할금액: 초기값0원';
COMMENT ON COLUMN "MEMBER"."MY_INFO_INTRO" IS '내 소개글';
COMMENT ON COLUMN "MEMBER"."MY_INFO_GIT" IS '깃허브 주소';
COMMENT ON COLUMN "MEMBER"."MY_INFO_HOMEPAGE" IS '노션, 포트폴리오 등 주소';
COMMENT ON COLUMN "MEMBER"."BEANS_AMOUNT" IS '커피콩지갑';
COMMENT ON COLUMN "MEMBER"."CURRENT_EXP" IS '회원 현재 경험치';
COMMENT ON COLUMN "MEMBER"."MEMBER_LEVEL" IS 'LV1 ~ LV30';


-- 시퀀스 생성
DROP SEQUENCE SEQ_MEMBER_NO; 
CREATE SEQUENCE SEQ_MEMBER_NO
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- AUTH 테이블 생성
CREATE TABLE AUTH (
    AUTH_NO NUMBER NOT NULL,
    CODE VARCHAR2(100) NOT NULL,
    EMAIL VARCHAR2(100) NOT NULL,
    CREATE_AT DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT PK_AUTH PRIMARY KEY (AUTH_NO)
);
COMMENT ON COLUMN "AUTH"."AUTH_NO" IS '시퀀스번호';
COMMENT ON COLUMN "AUTH"."CODE" IS '인증키 코드';
COMMENT ON COLUMN "AUTH"."EMAIL" IS '이메일';
COMMENT ON COLUMN "AUTH"."CREATE_AT" IS '생성시간';

DROP SEQUENCE SEQ_AUTH_NO; 
CREATE SEQUENCE SEQ_AUTH_NO
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;


-- SOCIAL_LOGIN 테이블 생성
CREATE TABLE SOCIAL_LOGIN (
    SOCIAL_NO NUMBER NOT NULL,
    PROVIDER VARCHAR2(30) NOT NULL,
    PROVIDER_ID VARCHAR2(100) NOT NULL,
    MEMBER_NO NUMBER NOT NULL,
    CONSTRAINT PK_SOCIAL_LOGIN PRIMARY KEY (SOCIAL_NO),
    CONSTRAINT FK_MEMBER_TO_SOCIAL_LOGIN FOREIGN KEY (MEMBER_NO) REFERENCES MEMBER(MEMBER_NO),
    CONSTRAINT UK_SOCIAL_LOGIN UNIQUE (PROVIDER, PROVIDER_ID)
);

COMMENT ON COLUMN SOCIAL_LOGIN.SOCIAL_NO IS '시퀀스번호';
COMMENT ON COLUMN SOCIAL_LOGIN.PROVIDER IS 'KAKAO';
COMMENT ON COLUMN SOCIAL_LOGIN.PROVIDER_ID IS '식별 아이디';
COMMENT ON COLUMN SOCIAL_LOGIN.MEMBER_NO IS '회원번호(SEQ_MEMBER_NO)';

CREATE SEQUENCE SEQ_SOCIAL_LOGIN_NO
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- 확인
SELECT table_name FROM user_tables WHERE table_name = 'SOCIAL_LOGIN';
SELECT sequence_name FROM user_sequences WHERE sequence_name = 'SEQ_SOCIAL_LOGIN_NO';

-------------------------------------------------------------------------------
------------ 더미데이터 삽입 ---------------------------------------------------
-------------------------------------------------------------------------------
-- 기본 레벨 데이터 삽입
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (1,   0,     '초보자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (2,   100,   '견습 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (3,   300,   '연습생');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (4,   600,   '신입 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (5,   1000,  '튜토리얼 완료');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (6,   1500,  '초급 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (7,   2100,  '기능 사용자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (8,   2800,  '로직 사용자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (9,   3600,  '문제 해결가');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (10,  4500,  '주니어 개발자');

INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (11,  5500,  '숙련자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (12,  6600,  '기능 숙련자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (13,  7800,  '코드 숙련자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (14,  9100,  '실전 숙련자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (15, 10500,  '실무 숙련자');

INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (16, 12000,  '중급 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (17, 13600,  '설계 참여자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (18, 15300,  '안정성 담당');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (19, 17100,  '품질 담당');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (20, 19000,  '베테랑 개발자');

INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (21, 21000,  '고급 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (22, 23100,  '시스템 전문가');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (23, 25300,  '문제 해결 전문가');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (24, 27600,  '핵심 멤버');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (25, 30000,  '시니어 개발자');

INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (26, 32500,  '마스터');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (27, 35100,  '그랜드 마스터');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (28, 37800,  '전설의 개발자');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (29, 40600,  '서버 네임드');
INSERT INTO LEVELS (LEVEL_NO, REQUIRED_TOTAL_EXP, TITLE) VALUES (30, 43500,  '레전드');

COMMIT;

-- =========================================================================
-- 회원 더미데이터 
INSERT INTO MEMBER VALUES (
  0,'admin@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '관리자','Administrator','0101000001','전설',
  'N','Y',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  10000000,100000,30
);
INSERT INTO MEMBER VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user01@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '김도현','NullMaster','0101000001','웹백엔드 개발자 1년차',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  1000,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user02@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '이서연','버그헌터','0101000002','프론트엔드 개발자 6개월',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  0,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user03@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '박지훈','코딩하는곰','0101000003','풀스택 개발자 2년차',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  30,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user04@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '최민재','SQL마법사','0101000004','DBA/데이터엔지니어 3년차',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user05@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '정윤호','디버깅중독','0101000005','백엔드 개발자 1년차(Spring)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user06@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '한지수','콘솔로그장인','0101000006','프론트엔드 개발자 2년차(React)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user07@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '오현우','에러수집가','0101000007','QA 엔지니어 1년차(테스트 자동화)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user08@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '유채원','주석요정','0101000008','웹퍼블리셔 8개월(접근성/반응형)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user09@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '강민수','메모리도둑','0101000009','시스템 엔지니어 4년차(Linux/네트워크)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);

INSERT INTO MEMBER  VALUES (
  SEQ_MEMBER_NO.NEXTVAL,'user10@joboju.com','$2a$10$XVUq9irjRcTuzgfvXeq9HuFdZf4RAJvcGQVj1Qzc20BD/ShnF0o7u',
  '신예린','리팩터여신','0101000010','풀스택 개발자 3년차(Java+JS)',
  'N','N',NULL,'N',SYSDATE,
  0,NULL,NULL,NULL,
  100,0,1
);


-- 1) 보드코드 테이블 데이터 추가
INSERT INTO BOARDTYPE
(BOARD_CODE, BOARD_NAME, PARENTS_BOARD_CODE)
VALUES (1, 'ITT', NULL);

INSERT INTO BOARDTYPE
(BOARD_CODE, BOARD_NAME, PARENTS_BOARD_CODE)
VALUES (2, 'IndustryNews', NULL);

INSERT INTO BOARDTYPE
(BOARD_CODE, BOARD_NAME, PARENTS_BOARD_CODE)
VALUES (3, 'Freeboard', NULL);

COMMIT;
