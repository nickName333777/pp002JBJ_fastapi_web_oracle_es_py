# pp002JBJ_fastapi_web_oracle_es_py

# 📁 프로젝트 디렉토리 구조

```
pp002JBJ_fastapi_web_oracle_es_py/
│
├── 📄 main.py                      # FastAPI 메인 애플리케이션
├── 📄 database.py                  # DB 연결 설정
├── 📄 models.py                    # SQLAlchemy 모델
├── 📄 schemas.py                   # Pydantic 스키마
├── 📄 auth.py                      # JWT 인증 유틸리티
├── 📄 member_router.py             # 회원 라우터
├── 📄 email_router.py              # 이메일 라우터
├── 📄 kakao_router.py              # 카카오 소셜 로그인 라우터
├── 📄 kakao_schemas.py             # 카카오 소셜 로그인 Pydantic 스키마
├── 📄 kakao_service.py             # 카카오 소셜 로그인 서비스
│
├── 📄 requirements.txt             # Python 의존성
├── 📄 Dockerfile                   # FastAPI 컨테이너 설정
├── 📄 docker-compose.yml           # Docker Compose 설정
├── 📄 .env                         # 환경 변수 (git ignore)
├── 📄 .env.example                 # 환경 변수 예시
├── 📄 .gitignore                   # Git ignore 설정
├── 📄 README.md                    # 프로젝트 문서
│
├── 📁 docs/adr/                	  # SpringBoot->FastAPI 포팅 히스토리
│   ├── 📄 s001_loginSignUp_Prompt.mdown # login/signup 포팅
│   ├── 📄 s002_kakaoLogin_Prompt.mdown # 카카오 소셜 로그인 포팅
│   ├── 📄 s003_Answer_loginSignUp_kakaoLogin.mdown # s001~s002 단계에서 진행된 porting의 결과들
│   └── 📄 s007_freeboard_Prompt.mdown # 자유게시판/댓글 CRUD 포팅
│
├── 📁 init_scripts/                # DB 초기화 스크립트
│   ├── 📄 init_CDB_XE.sql          # Container DB(XE) 초기화 스크립트
│   └── 📄 init_PDB_XEPDB1.sql      # PDB (XEPBD1) 초기화 스크립트
│
├── 📁 static/                      # 프론트엔드 정적 파일
│   ├── 📄 index.html
│   ├── 📄 login.html
│   ├── 📄 signup.html
│   ├── 📄 signupKakao.html
│   │
│   ├── 📁 css/
│   │   ├── 📄 common.css
│   │   ├── 📄 main.css
│   │   ├── 📄 login.css
│   │   └── 📄 signup.css
│   │
│   ├── 📁 js/
│   │   ├── 📄 common.js
│   │   ├── 📄 main.js
│   │   ├── 📄 login.js
│   │   ├── 📄 signup.js
│   │   └── 📄 signupKakao.js
│   │
│   └── 📁 images/
│       ├── 🖼️ favicon.ico
│       └── 🖼️ jbj_logo.png
│
└── 📁 logstash/                    # Logstash 설정 (선택)
    ├── 📁 config/
    │   └── 📄 logstash.yml
    └── 📁 pipeline/
        └── 📄 logstash.conf
```

## 🔧 파일별 설명

### Backend (Python/FastAPI)

| 파일 | 설명 |
|------|------|
| `main.py` | FastAPI 애플리케이션 엔트리포인트, 라우터 등록 |
| `database.py` | Oracle DB 연결 및 세션 관리 |
| `models.py` | SQLAlchemy ORM 모델 (Member, Level, Auth) |
| `schemas.py` | Pydantic 스키마 (요청/응답 검증) |
| `auth.py` | JWT 토큰 생성/검증, 비밀번호 해싱 |
| `member_router.py` | 회원가입/로그인/중복체크 API |
| `email_router.py` | 이메일 인증 API |
| ` ` |  |
| `kakao_router.py` | 카카오 소셜 로그인 라우터 |
| `kakao_schemas.py` | 카카오 소셜 로그인 Pydantic 스키마 |
| `kakao_service.py` | 카카오 소셜 로그인 서비스 |


### Frontend (HTML/CSS/JS)

| 파일 | 설명 |
|------|------|
| `index.html` | 메인 페이지 |
| `login.html` | 로그인 페이지 |
| `signup.html` | 회원가입 페이지 |
| `signupKakao.html` | 카카오 소셜로그인 필수회원 정보 입력 페이지 |
| `common.css` | 공통 스타일 (헤더, 푸터, 네비게이션) |
| `main.css` | 메인 페이지 전용 스타일 |
| `login.css` | 로그인 페이지 전용 스타일 |
| `signup.css` | 회원가입 페이지 전용 스타일 |
| `common.js` | 공통 유틸리티 (인증, API 호출) |
| `main.js` | 메인 페이지 로직 |
| `login.js` | 로그인 로직 |
| `signup.js` | 회원가입 로직 |
| `signupKakao.js` | 카카오 소셜 로그인 필수 회원정보 입력 로직 |

### Docker & Infrastructure

| 파일 | 설명 |
|------|------|
| `Dockerfile` | FastAPI 컨테이너 이미지 빌드 설정 |
| `docker-compose.yml` | 전체 스택 오케스트레이션 |
| `.env` | 환경 변수 (실제 값, git ignore) |
| `.env.example` | 환경 변수 템플릿 |
| `init.sql` | Oracle DB 초기화 SQL |

## 🚀 시작하기

### 1. 필수 요구사항

- Docker Desktop (최신 버전)
- Docker Compose (최신 버전)
- Git

### 2. 프로젝트 클론

```bash
git clone <repository-url>
cd pp002JBJ_fastapi_web_oracle_es_py
```

### 3. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 설정을 수정합니다:

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 실제 값으로 변경:

```env
# Database
DB_USER=your_user
DB_PASSWORD=your_pass123
DB_HOST=oracle-db
DB_PORT=1521
DB_SERVICE=XEPDB1

# JWT Secret (최소 32자 이상)
SECRET_KEY=your-very-long-secret-key-at-least-32-characters-long

# Email (Gmail 사용 시)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

# Oracle Admin Password
ORACLE_PWD=OracleAdmin123
```

### 4. 정적 파일 준비

`static/images/` 디렉토리에 로고 이미지를 배치:

```bash
mkdir -p static/images
# jbj_logo.png 파일을 static/images/ 폴더에 복사
```

### 5. 데이터베이스 초기화

(옵션1) Oracle 컨테이너가 완전히 시작된 후 (약 2-3분 소요):

```bash
# Oracle 컨테이너 접속
docker exec -it jbj-oracle bash

 
# 도커 bash에서 SQL*Plus로 접속
sqlplus sys/YourSecurePassword123@//localhost:1521/XEPDB1 as sysdba

# 사용자 생성
CREATE USER jbj_user IDENTIFIED BY jbj_pass123;
GRANT CONNECT, RESOURCE, DBA TO jbj_user;
ALTER USER jbj_user QUOTA UNLIMITED ON USERS;

# 생성한 사용자로 접속
CONNECT jbj_user/jbj_pass123@//localhost:1521/XEPDB1

# init.sql 스크립트 실행
@/opt/oracle/scripts/startup/init.sql

# 확인
SELECT * FROM LEVELS;
```


(옵션2)
```bash
# 또는, Oracle 컨테이너가 완전히 시작된 후[약간 다름]:
docker exec -it jbj-oracle sqlplus sys/YourSecurePassword123@//localhost:1521/XEPDB1 as sysdba

# SQL*Plus에서
CREATE USER jbj_user IDENTIFIED BY jbj_pass123;
GRANT CONNECT, RESOURCE, DBA TO jbj_user;
ALTER USER jbj_user QUOTA UNLIMITED ON USERS;
exit;

# 사용자로 재접속
docker exec -it jbj-oracle sqlplus jbj_user/jbj_pass123@//localhost:1521/XEPDB1

# init.sql 실행
@/opt/oracle/scripts/startup/init.sql
exit;

```


(옵션3) 혹은 sqldeveloper에서 아래 것들을 수행해도 된다.
```sqldeveloper

------------------------------------------------------------
-- PDB (Pluggable DB, 서비스name: XEPDB1) 용 유저 생성 by 관리자
-- [여기부터 4줄 관리자 계정접속해서 PDB(XEPDB1)에 'jbj_user'계정 생성]
------------------------------------------------------------


-- 1. 관리자 계정(sys as sysdba)으로 접속
-- 관리자 계정임을 확인
SELECT USER FROM dual;
-- 'SYS' 나와야함

-- 2. CDB$ROOT로 이동 후 새 PDB (XEPDB1) 생성
-- 2-0) CDB 루트에서 실행
ALTER SESSION SET CONTAINER = CDB$ROOT;
SHOW CON_NAME; 
-- CDB$ROOT 나옴

-- CDB 레벨 확인
SELECT 'CDB (XE)' as location, username, account_status, common 
FROM cdb_users;
--WHERE username = 'JBJ_USER'; # 'JBJ_USER'가 CDB, PDB에 각각 하나씩 있을 수 있으나, 이름만 같을뿐 별개의 nampespace

-- 2-1) 모든 PDB 목록 확인
SHOW PDBS;
SELECT name, open_mode FROM v$pdbs;

-- 2-2) XEPDB1 생성 (admin 사용자 포함)
CREATE PLUGGABLE DATABASE XEPDB1 
ADMIN USER xepdb1_admin IDENTIFIED BY xepdb1_pass123
ROLES=(CONNECT, RESOURCE, DBA)
FILE_NAME_CONVERT=(
  '/opt/oracle/oradata/XE/pdbseed/',
  '/opt/oracle/oradata/XE/XEPDB1/'
);

-- 2-3) PDB 열기
ALTER PLUGGABLE DATABASE XEPDB1 OPEN;

-- 3. 새 PDB로 접속 테스트
ALTER SESSION SET CONTAINER = XEPDB1;
SHOW CON_NAME;  
-- "XEPDB1" 나옴

-- 모든 사용자 계정 조회
SELECT username FROM dba_users;
-- 기존 사용자 삭제 (테이블 등 객체도 함께 삭제)
DROP USER jbj_user CASCADE;
-- 기존 사용자 삭제 확인
SELECT username FROM dba_users WHERE username = 'JBJ_USER';
-- 아무 결과도 안 나오면 성공

-- 새 사용자 생성
CREATE USER jbj_user IDENTIFIED BY jbj_pass123;
--GRANT CONNECT, RESOURCE, CREATE TABLE TO jbj_user;
-- 권한 부여
GRANT CONNECT, RESOURCE, CREATE VIEW TO jbj_user;
-- CONNECT : DB 연결 권한 ROLE (SET CONTAINER, CREATE SESSION; 2개 권한)
-- RESOURCE : DB 기본 객체 생성 권한 ROLE (CREATE INDEXTYPE, 
                   --  CREATE OPERATOR, CREATE TYPE, CREATE TRIGGER,
                   --  CREATE PROCEDURE, CREATE SEQUENCE, CREATE CLUSTER
                   -- CREATE TABLE; 8개 권한)
-- 객체 생성 공간 할당성QUOTA UNLIMITED ON SYSTEM;
--ALTER USER jbj_user DEFAULT TABLESPACE SYSTEM
--QUOTA UNLIMITED ON SYSTEM;
ALTER USER jbj_user DEFAULT TABLESPACE USERS
                    TEMPORARY TABLESPACE TEMP
                    QUOTA UNLIMITED ON USERS;

COMMIT;

-- 확인
SELECT username, account_status, common
FROM dba_users 
WHERE username = 'JBJ_USER';

-- 현재 PDB 확인
SHOW CON_NAME;
-- XEPDB1 나옴

-- XEPDB1 레벨 확인
SELECT 'PDB (XEPDB1)' as location, username, account_status, common 
FROM dba_users;
--WHERE username = 'JBJ_USER';

-- 모든 PDB 목록 확인 (CDB 보다는 적은 목록확인 가능)
SHOW PDBS;
SELECT name, open_mode FROM v$pdbs;

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- ### 추천: 일반 작업용 연결은 PDB(XEPDB1) 사용 + 개발/관리용 연결은 SQL Developer로 관리
-- ['jbj_user'계정 젒속하여 init.sql 실행]
--
--
---- SQL Developer로 XEPDB1의 사용자도 관리: SQL Developer로 XEPDB1 접속 설정
-- 새 연결 추가 (PDB 전용)
-- SQL Developer에서:
--```
--Connection Name: Oracle21c_XEPDB1
--Username: jbj_user
--Password: jbj_password1234
--Connection Type: Basic
--Hostname: localhost
--Port: 1521
--Service name: XEPDB1  ← 이게 중요!
--```
```



### 6-A. Docker Compose 실행 [옵션 A]
==> docker_compose_sov02_yml_전체도커서비스실행시.txt 참조

```bash
# 모든 서비스 시작(옵션1) => docker_compose_sov02_yml_전체도커서비스실행시.txt 참조
docker-compose up -d # (옛날 v1 (별도 패키지))
docker compose up -d # (현재 표준 (v2, Docker CLI 플러그인))

## 빌드 및 시작
#docker-compose up --build -d # (옛날 v1 (별도 패키지))
#docker compose up --build -d # 현재 표준 (v2, Docker CLI 플러그인))
# Oracle 제외하고 나머지만 실행(옵션2)
docker-compose up -d fastapi-backend elasticsearch kibana logstash # (옛날 v1 (별도 패키지))
docker compose up -d fastapi-backend elasticsearch kibana logstash # 현재 표준 (v2, Docker CLI 플러그인))

# 로그 확인
docker-compose logs -f fastapi-backend # (옛날 v1 (별도 패키지))
docker compose logs -f fastapi-backend # 현재 표준 (v2, Docker CLI 플러그인))
#docker-compose logs -f oracle-db # (옛날 v1 (별도 패키지))
#docker-compose logs -f elasticsearch
#docker-compose logs -f kibana
#docker compose logs -f logstash
#docker compose logs -f oracle-db # 현재 표준 (v2, Docker CLI 플러그인))
#docker compose logs -f elasticsearch
#docker compose logs -f kibana
#docker compose logs -f logstash
## 로그 확인
#docker-compose logs -f # (옛날 v1 (별도 패키지))
#docker compose logs -f # 현재 표준 (v2, Docker CLI 플러그인))
```


### 6-B. 기존 oracle21c 컨테이너 계속 사용 [옵션 B]
==> docker-compose.yml 참조

docker-compose.yml에서 새로 정의한 oracle-db 또는 jbj-oracle 컨테이너를 사용하지 않고, 이전에 Moa, Devlog프로젝트에서 계속 사용했던 docker 'oracle21c' 컨테이너를 여기서도 계속 사용하고자 할 경우 아래 순서대로 실행하면 된다.


```bash

# 1. 기존 Oracle 시작
docker start oracle21c

# 2. .env 파일 설정 (-> 이건 이미 .env에 반영되어 있음)
cat > .env << EOF
DB_HOST=oracle21c
DB_PASSWORD=jbj_pass123
DB_USER=jbj_user
DB_PORT=1521
DB_SERVICE=XEPDB1
EOF

# 3. docker compose 네트워크 생성
docker compose up -d --no-start # 현재 표준 (v2, Docker CLI 플러그인))

# 4. docker compose 네트워크 확인
docker network ls | grep jbj

# 5. Oracle(oracle21c)을 네트워크에 연결
#docker network connect jbj-fastapi_jbj-network oracle21c
docker network connect pp002jbj_fastapi_web_oracle_es_py_jbj-network oracle21c

# 6. docker-compose에서 Oracle 제외하고 실행(나머지 서비스 시작)
# (이걸 먼저 시작하면 나머지 서비스 실행되면서 docker-compose 네크워크가 생성되므로 3번의 네트워크 연결을 이 다음에 해도 된다.)
docker compose up -d fastapi-backend elasticsearch kibana

# 7. 네트워크 연결 확인
docker exec -it jbj-fastapi ping -c 3 oracle21c # 만약 error exec: "ping": executable file not found in $PATH ==>Dockerfile에서 FROM python:3.10-slim => FROM python:3.10로하고 추가 유틸리티 설치(Dockerfile참조)

#docker run -it pp002jbj_fastapi_web_oracle_es_py-fastapi-backend bash # run from the image

# 8. 웹 접속
curl http://localhost:8000/health
(예상결과: {"status": "healthy", "database": "connected"})

# 9. 연결 테스트
docker logs jbj-fastapi

# 10. Python에서 직접 테스트
python -c "
import cx_Oracle
try:
    conn = cx_Oracle.connect('jbj_user/jbj_pass123@oracle21c:1521/XEPDB1')
    print('✅ Oracle 연결 성공!')
    conn.close()
except Exception as e:
    print(f'❌ 연결 실패: {e}')
"

```
### 6-C. docker-compose.yml 실행 troubleshoot
#### 6-C-1. 컨테이너 상태확인1
- 컨테이너 진입: 

아래 cli 커맨드로 docker container안으로 진입(나오는건 도커 프롬프트#에서 #exit 또는 ctl-D)
$ docker run -it --rm python:3.10-slim bash

- 컨테이너 안

\# apt-get update
\#apt-get install -y wget unzip libaio1

#### 6-C-2. 컨테이너 상태확인2
docker exec -it jbj-fastapi bash # 컨테이너 bash에 진입한 후

ping oracle21c  # 네트워크 연결 확인

#### 6-C-3. 개발 vs 운영/배포
개발 환경 → python:3.10 (ping/curl/netstat 등 다 있음)
운영/배포 → python:3.10-slim + 필요한 유틸리티만 설치

\# 개발용 - 바로 사용 가능 (Ubuntu 기반 풀 버전: FROM python:3.10-focal)
FROM python:3.10

\# 또는 슬림 + 유틸리티만 추가 (중간 크기)
FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    iputils-ping curl net-tools vim htop \
    && rm -rf /var/lib/apt/lists/*

#### 6-C-4. Docker Compose로 재빌드하는 방법들:<br>
a. 특정 서비스만 재빌드 (가장 많이 씀)
<br>\# fastapi-backend 서비스만 재빌드
<br>docker compose build fastapi-backend
<br>docker compose build --no-cache fastapi-backend # 제일 중요! 기존 캐시 때문에 새 코드가 안 먹힘
<br>\# 재빌드 후 재시작
<br>docker compose up -d fastapi-backend

b. 강제 재빌드 + 재시작 (한 번에)
<br>\# Dockerfile 바뀌었을 때 강제로 재빌드
<br>docker compose up -d --build --force-recreate fastapi-backend

c. 모든 서비스 재빌드
<br>docker compose build
<br>docker compose up -d

d. 기존 컨테이너 완전 삭제 후 재빌드 (깔끔하게)
<br>docker compose down
<br>docker compose up -d --build

e. 기존 코드 캐쉬에 남아서 안먹힐때.

강제 재빌드:
<br>docker compose down fastapi-backend
<br>docker compose build --no-cache fastapi-backend
<br>docker compose up -d fastapi-backend
<br> 
<br>컨테이너 안에서 Oracle Client 설치 확인:
<br>docker exec -it jbj-fastapi bash
<br>ls -la /opt/oracle/
<br>echo $LD_LIBRARY_PATH
<br>ldconfig -p | grep oracle

#### 6-C-5. 다른 컨테이너가 아직 네트워크에 붙어서, 네트워크가 "Resource is still in use" 상태라 제거되지 않을 때: 네트워크 완전 제거 후 재생성해야 한다.

1. 모든 컨테이너 완전 중지
<br>docker compose down

2. 남은 컨테이너들 확인 후 제거
<br>\# 네트워크에 붙은 컨테이너 확인
<br>docker network ls
<br>docker network inspect pp002jbj_fastapi_web_oracle_es_py_jbj-network
<br>\# 모든 컨테이너 중지&제거 (강제)
<br>docker stop $(docker ps -aq)
<br>docker rm $(docker ps -aq)

3. 네트워크 강제 삭제
<br>\# 네트워크 이름 확인
<br>docker network ls
<br>\# 해당 네트워크 강제 삭제
<br>docker network rm pp002jbj_fastapi_web_oracle_es_py_jbj-network

4. 한 번에 깔끔하게 정리 (추천)
<br>\# 모든 도커 리소스 정리
<br>docker compose down -v --remove-orphans --rmi all
<br>\# 또는 모든 미사용 네트워크&컨테이너 정리
<br>docker network prune -f
<br>docker container prune -f

5. 재빌드 & 재시작
<br>docker compose build --no-cache fastapi-backend
<br>docker compose up -d

🚀 가장 빠른 해결책 (한 줄) <=======!!!!!

<br>docker compose down --volumes --remove-orphans && docker network prune -f && docker compose up -d --build --force-recreate

이렇게 하면 네트워크 완전 삭제 → 새로 생성 → 컨테이너 재빌드까지 한 번에 해결된다. 프로젝트 폴더명 기반으로 자동 생성된 네트워크는 위 명령어만으로 완벽히 정리된다.

( 또는, fastapi-backend만 업데이트할 경우에 유용!!! ===> 
<br>docker compose down && docker rmi $(docker images -q '*fastapi*') && docker compose build --no-cache fastapi-backend && docker compose up -d fastapi-backend
<br>docker compose build --no-cache 꼭 해야 캐시 때문에 새 코드가 무시된다!)

#### 6-C-6. 로그인 denied 이슈: 

$sqlplus jbj_user/jbj_password1234@XEPDB1 실행 시 login denied 나올 경우 이유는:

1. CDB(Container DB, 서비스명:XE)에 sqldeveloper를 이용하여 jbj_user/password를 등록하였지만 PDB(Pluggable DB, 서비스명:XEPDB1)에는 jbj_user가 등록되어 있지 않은 경우 => 두 연결 모두 각각  가능하고, 서로 독립적인 것임에 유의!!. CDB와 PDB는 **완전히 다른 네임스페이스**.
```
CDB (XE):
  └── jbj_user (SQL Developer로 만든 것)

PDB (XEPDB1):
  └── jbj_user (새로 만들 것 - FastAPI용) by 도커bash cli또는 sqldeveloper

```

2. XEPDB1이 tnsnames.ora에 제대로 등록되지 않았을 가능성

Oracle 21c Express는 기본적으로 XEPDB1 PDB(Pluggable Database)를 제공하지만
tnsnames.ora 파일에 제대로 설정되어 있지 않으면 연결 실패
tnsnames.ora 파일 설정을 확인하는 명령어:
\# tnsnames.ora 파일 확인:
$ docker exec -it oracle21c bash -c "
cat /opt/oracle/product/21c/dbhomeXE/network/admin/tnsnames.ora
"

3. Easy Connect 방식으로 접속해야 함
Oracle Express Edition에서는 Easy Connect String을 사용하는 게 더 안전해:
bash# ❌ 작동 안 할 수 있으므로 
sqlplus jbj_user/jbj_pass123@XEPDB1 을 사용하지 말고, 이렇게 해야 함
sqlplus jbj_user/jbj_pass123@//localhost:1521/XEPDB1

4. DB 초기화
docker exec -i oracle21c sqlplus jbj_user/jbj_pass123@//localhost:1521/XEPDB1 < init_scripts/init_PDB_XEPDB1.sql



#### 6-C-7. 사용하지 않는 untagged 이미지(특히 dangling 이미지)를 지우는 대표적인 명령어

1. dangling(태그·레포 없음) 이미지 삭제: 가장 안전한 방법:

<br>현재 어떤 컨테이너에서도 사용하지 않는 “dangling” 이미지를 삭제한다.​확인 질문이 나오면 y 입력.
<br>$ docker image prune

<br>강제로(확인 없이) 지우고 싶으면:
<br>$ docker image prune -f

2. 모든 untagged 이미지 삭제: (untagged) 이미지를 전부 지우고 싶다면:

<br>먼저 목록 확인
<br>$ docker images -f "dangling=true" 

<br>-q 옵션은 이미지 ID만 출력해서, 그걸 docker rmi에 넘겨 한 번에 삭제하는 방식이다.
<br>$ docker rmi $(docker images -f "dangling=true" -q) 
​

3. 완전 정리(안 쓰는 모든 이미지 삭제): 사용되지 않는 이미지들 다 정리
<br>$ docker image prune -a 
<br>현재 어떤 컨테이너에서도 사용하지 않는 모든 이미지를 삭제한다.
(​실행 전에 꼭 docker ps -a로 필요한 컨테이너/이미지 있는지 확인하는 것이 좋다.)

4. 특정 이미지만 지우려면 docker rmi(또는 docker image rm) 명령어에 이미지 이름:태그 또는 이미지 ID를 넣어서 삭제하면 된다.

<br> 이미지 이름:태그로 삭제 =>  $docker rmi REPOSITORY:TAG

<br> 예: python:3.10-slim 삭제 => $docker rmi python:3.10-slim

<br> 이미지 ID로 삭제 => $ docker rmi IMAGE_ID

<br> 예: ID가 0fb4f4cf454f 인 이미지 삭제=> $ docker rmi 0fb4f4cf454f
<br> 사용 중일 때 에러 나는 경우: 해당 이미지를 사용하는 컨테이너가 있으면 삭제가 안 되고 에러가 난다. 이때는:

<br>컨테이너 정지: docker stop 컨테이너ID
<br>컨테이너 삭제: docker rm 컨테이너ID
<br>그다음 다시 docker rmi 이미지ID 실행.
​<br>
<br>강제로 삭제 (주의) ==> $ docker rmi -f IMAGE_ID
<br>강제 삭제 옵션이어서, 다른 데서 쓰고 있는 이미지를 억지로 지울 수 있어 실수하면 환경 깨질 수 있으니 주의해서 사용.
​
#### 6-C-8. FastAPI debugging 재시작 필요 여부 요약표

| 변경 사항  | 재시작 필요?| 명령어|
|---|---|---|
|Python 코드 (.py)|❌ 불필요|자동 리로드|
|Static 파일 (HTML/CSS/JS)|❌ 불필요|브라우저 새로고침|
|.env 파일|⚠️ restart만|docker-compose restart fastapi-backend|requirements.txt|✅ 필요|docker-compose build fastapi-backend && docker-compose up -d
|Dockerfile|✅ 필요|docker-compose down && docker-compose build --no-cache && docker-compose up -d
|docker-compose.yml|✅ 필요|docker-compose down && docker-compose up -d|

#### 개발워크플로우
1. 도커 시작
	<br>$docker compose up -d
	
2. 개발 시작	
	<br>$docker logs -f jbj-fastapi  # 터미널 1

3. 코드 수정 (VS Code 또는 gedit): → 저장 → 로그에서 "Reloading..." 확인

4. API 테스트 (터미널 2)
	<br>$curl http://localhost:8000/member/login ...

5. 브라우저 테스트: → F12 → Network 탭 → 요청 확인

6. 문제 발생 시: → 로그 확인 → DB 직접 확인 → Python shell에서 직접 테스트

7. 하루 작업 종료
	<br>$docker-compose down


### 7. oracle, elasticsearch 호스트 마운트 폴더 권한 맞추기

#### oracle: 
```bash
# 소유자 확인
ls -la /home/oracle/

# 권한 부여 (필요시)
sudo chown -R 54321:54321 /home/oracle/oradata
sudo chmod -R 755 /home/oracle/oradata
```

#### elasticsearch:
Elasticsearch 컨테이너 기본 권한 개념
- 공식 Elasticsearch 도커 이미지는 컨테이너 내부에서 보통 UID 1000, GID 0(root 그룹) 또는 1000:1000 으로 실행된다.
- 호스트 디렉터리를 바인드 마운트(/home/elasticsearch/esdata:/usr/share/elasticsearch/data) 하면, 컨테이너 안 프로세스 UID/GID 가 호스트 디렉터리에도 쓰기 권한이 있어야 한다.
​
```bash

# 폴더 생성:
sudo mkdir -p /home/elasticsearch/esdata
ls -la /home/elasticsearch/

# 실제 UID/GID 는 컨테이너를 한 번 띄운 뒤 다음처럼 확인
docker exec -it jbj-elasticsearch id

# 권한 부여 (필요시)
# 1) UID/GID 맞춰서 chown (권장): 대부분의 경우 아래 둘 중 하나가 맞는다.
	# 컨테이너가 1000:0 으로 동작하는 경우:
	sudo chown -R 1000:0 /home/elasticsearch/esdata
	# 컨테이너가 1000:1000 으로 동작하는 경우:
	sudo chown -R 1000:1000 /home/elasticsearch/esdata
# 2) rwx권한
	sudo chmod -R 755 /home/elasticsearch/esdata
```


### 8. 애플리케이션 접속

- **메인 페이지**: http://localhost:8000
- **로그인 페이지**: http://localhost:8000/login.html
- **회원가입 페이지**: http://localhost:8000/signup.html
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200

## 🧪 테스트 절차

### 1. 회원가입 테스트

1. http://localhost:8000/signup.html 접속
2. 이메일 입력 및 인증번호 받기
3. 받은 인증번호 입력 및 인증
4. 나머지 필수 정보 입력
5. "가입 하기" 버튼 클릭
6. 성공 메시지 확인 후 로그인 페이지로 이동

### 2. 로그인 테스트

1. http://localhost:8000/login.html 접속
2. 가입한 이메일과 비밀번호 입력
3. "아이디 저장" 체크 (선택)
4. "로그인" 버튼 클릭
5. 메인 페이지로 리다이렉트 확인
6. 헤더에 사용자 닉네임 표시 확인

### 3. API 테스트 (Swagger 사용)

http://localhost:8000/docs 에서 다음 API 테스트:

- `POST /member/signup` - 회원가입
- `POST /member/login` - 로그인
- `GET /member/dupcheck/email` - 이메일 중복 체크
- `GET /member/dupcheck/nickname` - 닉네임 중복 체크
- `GET /sendEmail/signup` - 인증 이메일 발송
- `GET /sendEmail/checkAuthKey` - 인증번호 확인

## 🛠️ 문제 해결

### Oracle 컨테이너가 시작되지 않는 경우

```bash
# 컨테이너 로그 확인
docker logs jbj-oracle

# 포트 충돌 확인
lsof -i :1521

# 볼륨 초기화 후 재시작
docker-compose down -v
docker-compose up -d
```

### FastAPI 컨테이너가 Oracle에 연결되지 않는 경우

```bash
# Oracle 컨테이너 health check 확인
docker ps

# Oracle 서비스 준비 확인
docker exec jbj-oracle lsnrctl status

# FastAPI 재시작
docker-compose restart fastapi-backend
```

### 이메일 발송이 안 되는 경우

Gmail 사용 시:
1. Google 계정 보안 설정에서 "2단계 인증" 활성화
2. "앱 비밀번호" 생성
3. 생성된 앱 비밀번호를 `.env`의 `SMTP_PASSWORD`에 설정

## 📊 모니터링

### 서비스 상태 확인

```bash
# 모든 컨테이너 상태
docker-compose ps

# 특정 서비스 로그
docker-compose logs -f [service-name]

# 리소스 사용량
docker stats
```

### Elasticsearch 확인

```bash
# 클러스터 상태
curl http://localhost:9200/_cluster/health?pretty

# 인덱스 목록
curl http://localhost:9200/_cat/indices?v
```

## 🔄 개발 환경 설정

로컬에서 개발하는 경우:

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 후 실행
python main.py
```

## 📝 다음 단계

이번 단계에서 구현한 기능:
- ✅ 회원가입/로그인
- ✅ 이메일 인증
- ✅ JWT 토큰 인증
- ✅ 메인 페이지

다음 포팅 예정:
- ⏳ 자유게시판 (CRUD)
- ⏳ 댓글 시스템
- ⏳ 좋아요 기능
- ⏳ Elasticsearch 검색
- ⏳ AI 챗봇 통합



