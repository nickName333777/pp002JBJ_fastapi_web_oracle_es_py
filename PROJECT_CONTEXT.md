# 프로젝트 컨텍스트 문서

**최종 업데이트:** 2026년 1월 28일

---

## 🎯 프로젝트 목적

### SpringBoot 기반 웹 애플리케이션을 FastAPI 기반으로 완전 포팅

#### 원본 스택 (SpringBoot)
- **언어/프레임워크:** Java 17 + SpringBoot 3.5.7
- **ORM:** JPA/Hibernate (회원, 카카오 로그인) + MyBatis (게시판)
- **인증/보안:** Spring Security
- **템플릿 엔진:** Thymeleaf
- **데이터베이스:** Oracle Database 21c XE
- **검색엔진:** Elasticsearch (Docker)
- **개발환경:** STS4 IDE + Gradle

#### 목표 스택 (FastAPI)
- **언어/프레임워크:** Python 3.10 + FastAPI
- **ORM:** SQLAlchemy
- **인증/보안:** JWT (python-jose) + bcrypt
- **프론트엔드:** Native JavaScript (SPA 방식)
- **데이터베이스:** Oracle Database 21c XE (PDB: XEPDB1)
- **검색엔진:** Elasticsearch + Kibana + Logstash
- **배포:** Docker Compose 기반 풀스택

#### 핵심 철학
**단순 코드 변환이 아닌, "왜 이렇게 설계되었는지"와 "왜 이렇게 포팅되었는지" 이해 중심**

---

## 📊 현재 구현 상태

### ✅ 완료된 기능

#### 1. 회원가입/로그인 (일반) - s001 단계
**주요 기능:**
- 이메일 인증 기반 회원가입
  - 6자리 랜덤 인증번호 생성
  - 5분 만료 시간 체크
  - SMTP(Gmail) 이메일 발송
- JWT 토큰 기반 인증/인가 (유효기간 7일)
- 이메일/닉네임 중복 체크 (실시간 AJAX)
- 비밀번호 bcrypt 해싱
- 쿠키 기반 "아이디 저장" 기능
- 레벨 시스템 (1~10레벨, 경험치 기반)

**파일 구조:**
- Backend: `member_router.py`, `email_router.py`, `auth.py`, `models.py`, `schemas.py`
- Frontend: `login.html/css/js`, `signup.html/css/js`
- DB: MEMBER, LEVELS, AUTH 테이블

#### 2. 카카오 소셜 로그인 - s002 단계
**주요 기능:**
- OAuth 2.0 인증 플로우
- 카카오 사용자 정보 연동 (kakaoId 기반)
- SOCIAL_LOGIN 테이블 (복합 유니크: PROVIDER + PROVIDER_ID)
- 신규 사용자: 필수 정보 입력 (`signupKakao.html`)
- 기존 사용자: 자동 로그인
- 이메일 기반 일반/소셜 계정 통합 가능

**파일 구조:**
- Backend: `kakao_router.py`, `kakao_service.py`, `kakao_schemas.py`
- Frontend: `signupKakao.html/js` (CSS는 signup.css 공유)
- DB: SOCIAL_LOGIN 테이블

**설정 필요:**
- `.env`에 `KAKAO_REST_API_KEY`, `KAKAO_CLIENT_SECRET`, `KAKAO_REDIRECT_URI` 설정
- 카카오 개발자 콘솔에서 Redirect URI 등록 필요

#### 3. 인프라 구성
**Docker Compose 멀티 컨테이너:**
- **FastAPI backend** (jbj-fastapi)
  - Uvicorn auto-reload (개발 시 코드 수정 즉시 반영)
  - Volume mount: `.:/app`, `./static:/app/static`
  - Port: 8000
  
- **Oracle 21c XE** (oracle21c)
  - PDB: XEPDB1 사용 (CDB가 아닌 PDB 사용 이유: 격리, 멀티테넌트 최적화)
  - User: jbj_user / Password: jbj_password1234
  - Port: 1521
  
- **Elasticsearch** (jbj-elasticsearch)
  - Version: 8.11.0
  - Port: 9200
  
- **Kibana** (jbj-kibana)
  - Port: 5601
  
- **Logstash** (jbj-logstash)
  - Port: 5044 (현재 미사용)

**환경 변수 관리:**
- `.env` 파일로 민감 정보 관리
- `docker-compose.yml`에서 `env_file: .env` 참조

#### 4. 프론트엔드 아키텍처
**SPA 방식 (Static HTML + Native JS):**
- JWT 토큰 localStorage 저장
- `common.js`: API 호출 유틸리티, 인증 체크
- 공통 컴포넌트: header, footer, navigation
- 페이지별 독립 JS 모듈

**공통 컴포넌트:**
- `index.html` (메인 페이지)
- `common.css` (공통 스타일)
- `common.js` (API 호출, 인증 체크, 날짜 포맷 등)

---

#### 4. 자유게시판 CRUD - s007 단계 (진행 중)

**✅ 1단계 완료 (DB + 백엔드 API):**

**데이터베이스:**
- BOARDTYPE, BOARD, BOARD_IMG, BOARD_LIKE, COMMENT 테이블
- SEQ_BOARD_NO, SEQ_IMAGE_NO, SEQ_COMMENT_NO 시퀀스
- 인덱스: 게시판코드, 작성자, 작성일, 댓글

**백엔드:**
- SQLAlchemy 모델 (models_freeboard.py)
  - Oracle CLOB 타입 처리
  - 자기참조 관계 (대댓글)
  - CASCADE 삭제 설정
- Pydantic 스키마 (board_schemas.py)
  - Request/Response 검증
  - 재귀 댓글 구조
- FastAPI 라우터 (board_router.py)
  - GET /api/board/freeboard/list (목록 조회)
    - 페이징 (page, limit)
    - 검색 (keyword, search_type: title|content|author|all)
    - 정렬 (sort_by: recent|views|likes)
  - GET /api/board/freeboard/{board_no} (상세 조회)
    - 조회수 자동 증가
    - 좋아요 개수 + 사용자 좋아요 여부
    - 댓글 개수

**파일 구조:**
- DB: init_freeboard.sql
- Backend: models_freeboard.py, board_schemas.py, board_router.py

**✅ 2단계 완료 (프론트엔드 목록/상세):**

**목록 화면 (freeboardList.html/css/js):**
- 게시글 카드 레이아웃 (썸네일, 제목, 작성자, 통계)
- 검색 기능 (제목/내용/작성자/전체)
- 정렬 기능 (최신순/조회수순/좋아요순)
- 페이징 (최대 10개 페이지 버튼)
- 반응형 디자인
- 상대 시간 표시 (N분 전, N시간 전)

**상세 화면 (freeboardDetail.html/css/js):**
- 게시글 내용 표시 (제목, 본문, 작성자 정보)
- 이미지 갤러리 (순서대로 표시)
- 좋아요 버튼 UI (하트 아이콘, 개수)
- 작성자 전용 버튼 (수정/삭제)
- 댓글 섹션 UI 준비

**파일 구조:**
- Frontend: freeboardList.html/css/js, freeboardDetail.html/css/js

**⏳ 3단계 예정 (작성/수정/댓글/좋아요 API 연동):**
- 게시글 작성 (POST /api/board/freeboard) + Frontend
- 게시글 수정 (PUT /api/board/freeboard/{id}) + Frontend  
- 게시글 삭제 (DELETE /api/board/freeboard/{id})
- 이미지 업로드 처리
- 좋아요 토글 (POST /api/board/freeboard/{id}/like) + Frontend 연동
- 댓글 CRUD (GET/POST/PUT/DELETE) + Frontend

---

## 🔑 중요한 설계/포팅 결정

### 1. 아키텍처 변경

| 항목 | SpringBoot | FastAPI | 이유 |
|------|-----------|---------|------|
| 패턴 | MVC (서버사이드 렌더링) | REST API + SPA | 비동기 처리, 프론트 분리 |
| 템플릿 | Thymeleaf | Static HTML + JS | 클라이언트 사이드 렌더링 |
| 상태 관리 | 세션 기반 (서버 상태 저장) | JWT (Stateless) | RESTful 원칙, 확장성 |
| ORM | JPA/Hibernate + MyBatis | SQLAlchemy | Python 표준 ORM |
| 검증 | Bean Validation | Pydantic | 타입 힌트 기반 검증 |

### 2. 데이터베이스 설계

#### PDB(XEPDB1) vs CDB(XE) 선택
**PDB 사용 이유:**
- 격리: 애플리케이션별 독립적인 데이터베이스 환경
- 멀티테넌트 최적화: Oracle 12c 이후 권장 아키텍처
- 개발/운영 분리: PDB별로 환경 분리 용이
- 보안: CDB는 관리용, PDB는 애플리케이션용

**현재 테이블 구조:**

**회원 관련 (s001, s002):**
```
MEMBER (회원)
├── MEMBER_NO (PK)
├── MEMBER_EMAIL (UK)
├── MEMBER_LEVEL (FK → LEVELS.LEVEL_NO)
├── MEMBER_PW (bcrypt 해시)
├── MEMBER_NICKNAME
└── ...

LEVELS (레벨)
├── LEVEL_NO (PK)
├── REQUIRED_TOTAL_EXP
└── TITLE

AUTH (이메일 인증)
├── AUTH_NO (PK)
├── CODE (6자리)
├── EMAIL
└── CREATE_AT (5분 만료)

SOCIAL_LOGIN (소셜 로그인)
├── SOCIAL_NO (PK)
├── PROVIDER (kakao, google, naver)
├── PROVIDER_ID
├── MEMBER_NO (FK → MEMBER.MEMBER_NO)
└── UK(PROVIDER, PROVIDER_ID)
```

**자유게시판 관련 (s007):**
```
BOARDTYPE (게시판 타입)
├── BOARD_CODE (PK)
├── BOARD_NAME
└── PARENTS_BOARD_CODE (FK → BOARDTYPE.BOARD_CODE, 계층 구조)
  - 1: 공지사항
  - 2: 질문게시판
  - 3: 자유게시판
  - 4: FAQ

BOARD (게시글)
├── BOARD_NO (PK, SEQ_BOARD_NO)
├── BOARD_TITLE (VARCHAR2 300)
├── BOARD_CONTENT (CLOB)
├── B_CREATE_DATE (DATE)
├── B_UPDATE_DATE (DATE)
├── BOARD_COUNT (조회수)
├── BOARD_DEL_FL (Y/N, 소프트 삭제)
├── BOARD_CODE (FK → BOARDTYPE.BOARD_CODE)
├── MEMBER_NO (FK → MEMBER.MEMBER_NO)
└── NEWS_REPORTER (뉴스용 선택 필드)

BOARD_IMG (게시글 이미지)
├── IMG_NO (PK, SEQ_IMAGE_NO)
├── IMG_PATH (저장 경로)
├── IMG_ORIG (원본 파일명)
├── IMG_RENAME (변경된 파일명, UUID)
├── IMG_ORDER (0: 썸네일, 1~4: 서브)
└── BOARD_NO (FK → BOARD.BOARD_NO, ON DELETE CASCADE)

BOARD_LIKE (게시글 좋아요)
├── BOARD_NO (PK, FK → BOARD.BOARD_NO)
├── MEMBER_NO (PK, FK → MEMBER.MEMBER_NO)
└── 복합 PK (BOARD_NO, MEMBER_NO)

COMMENT (댓글)
├── COMMENT_NO (PK, SEQ_COMMENT_NO)
├── MEMBER_NO (FK → MEMBER.MEMBER_NO)
├── BOARD_NO (FK → BOARD.BOARD_NO)
├── PARENTS_COMMENT_NO (FK → COMMENT.COMMENT_NO, 대댓글)
├── C_CREATE_DATE (DATE)
├── COMMENT_CONTENT (VARCHAR2 2000)
├── COMMENT_DEL_FL (Y/N, 소프트 삭제)
├── SECRET_YN (Y/N, 비밀댓글)
└── MODIFY_YN (Y/N, 수정 여부)
```

**인덱스 (성능 최적화):**
```
IDX_BOARD_CODE → BOARD(BOARD_CODE)
IDX_BOARD_MEMBER → BOARD(MEMBER_NO)
IDX_BOARD_DATE → BOARD(B_CREATE_DATE DESC)
IDX_COMMENT_BOARD → COMMENT(BOARD_NO)
IDX_COMMENT_MEMBER → COMMENT(MEMBER_NO)
```

**시퀀스:**
```
SEQ_BOARD_NO → 게시글 번호
SEQ_IMAGE_NO → 이미지 번호
SEQ_COMMENT_NO → 댓글 번호
```


### 3. 인증 방식 변경

#### SpringBoot → FastAPI 변경 사항
- **SpringBoot:** Spring Security (세션 기반)
- **FastAPI:** python-jose (JWT 기반)

#### 로그인 플로우
1. 이메일/비밀번호 검증 (bcrypt)
2. JWT 토큰 생성 (유효기간 7일)
   - Payload: `memberNo`, `memberEmail`, `memberNickname`, `role`
3. 클라이언트: localStorage에 저장
4. 모든 API 요청 시 `Authorization: Bearer <token>` 헤더 포함
5. 서버: JWT 검증 후 요청 처리

### 4. 이메일 인증 플로우

**구현 방식:**
1. 사용자가 이메일 입력 후 "인증번호 받기" 클릭
2. 서버에서 6자리 랜덤 인증번호 생성
3. AUTH 테이블에 저장 (CREATE_AT 기준 5분 만료)
4. SMTP(Gmail)로 이메일 발송
5. 프론트에서 타이머 표시 (05:00 → 00:00)
6. 사용자가 인증번호 입력 후 "인증하기" 클릭
7. 서버에서 인증번호 + 만료 시간 검증
8. 성공 시 회원가입 진행

### 5. 카카오 로그인 통합 전략

**DB 구조:**
- 카카오 ID를 SOCIAL_LOGIN 테이블에 저장
- Member 테이블과 1:N 관계 (한 회원이 여러 소셜 계정 연동 가능)
- 복합 유니크 제약: (PROVIDER, PROVIDER_ID)

**로그인 플로우:**
1. 사용자가 "카카오 로그인" 버튼 클릭
2. FastAPI → 카카오 인증 서버로 리다이렉트
3. 카카오 로그인 성공 → 인가 코드 받음
4. FastAPI: 인가 코드로 액세스 토큰 요청
5. 액세스 토큰으로 사용자 정보(kakaoId) 조회
6. SOCIAL_LOGIN 테이블에서 kakaoId 검색
   - **기존 회원:** 자동 로그인 → 메인 페이지
   - **신규 회원:** 필수 정보 입력 페이지 → 회원가입 → 로그인

**이메일 매칭:**
- 카카오에서 제공하는 이메일과 일반 회원가입 이메일이 같으면 통합 가능
- 사용자가 원하면 소셜 로그인과 일반 로그인 모두 사용 가능

### 6. 파일 업로드 전략 (s007)

**이미지 업로드 규칙:**
- 최대 5장
- 첫 번째 이미지가 썸네일 (대표 이미지)
- 허용 포맷: image/* (jpg, png, gif, webp 등)
- 저장 위치: `/mnt/user-data/uploads/board/{boardNo}/` (예정)

**DB 저장:**
- BOARD_IMG 테이블에 메타데이터 저장
  - IMG_PATH, IMG_ORIG, IMG_RENAME, IMG_ORDER

**SQLAlchemy 주의사항:**
- Oracle CLOB 타입 처리 (BOARD_CONTENT)
- SEQUENCE 자동 증가 (SEQ_BOARD_NO, SEQ_IMAGE_NO, SEQ_COMMENT_NO)

### 7. 자유게시판 주요 설계 결정 (s007)

#### 페이징 전략
- **방식:** Offset-based pagination
- **기본값:** page=1, limit=10
- **최대값:** limit=50 (과도한 데이터 요청 방지)
- **장점:** 간단하고 Oracle에서 잘 지원
- **개선 가능:** Cursor-based pagination (대용량 데이터)

#### 검색 전략
- **현재:** SQL LIKE 연산자 사용
  - `BOARD_TITLE LIKE '%keyword%'`
  - `MEMBER_NICKNAME LIKE '%keyword%'` (JOIN)
- **개선 계획:** Elasticsearch 전문 검색 통합
  - 형태소 분석
  - 하이라이팅
  - 자동완성

#### 정렬 방식
- **최신순:** `ORDER BY B_CREATE_DATE DESC`
- **조회수순:** `ORDER BY BOARD_COUNT DESC`
- **좋아요순:** 서브쿼리로 COUNT 후 정렬

#### 좋아요 개수 조회
- **방식:** 매번 COUNT 쿼리 실행
- **이유:** 실시간 정확성 보장
- **개선 가능:** 
  - BOARD 테이블에 `like_count` 컬럼 추가
  - 트리거로 자동 업데이트
  - 캐싱 (Redis)

#### 댓글 구조
- **대댓글:** `PARENTS_COMMENT_NO` 자기참조
- **렌더링:** 재귀 구조 (Pydantic 모델)
- **삭제:** 소프트 삭제 (`COMMENT_DEL_FL = 'Y'`)
  - 내용은 "삭제된 댓글입니다"로 표시
  - 대댓글이 있으면 완전 삭제 불가

#### 이미지 순서 규칙
- **img_order = 0:** 썸네일 (대표 이미지)
  - 목록에서 표시
  - OpenGraph 메타 태그용
- **img_order = 1~4:** 서브 이미지
  - 본문에서 갤러리로 표시

#### 소프트 삭제 전략
- **게시글:** `BOARD_DEL_FL = 'Y'`
  - 목록/상세 조회 시 필터링
  - 관리자는 복구 가능
- **댓글:** `COMMENT_DEL_FL = 'Y'`
  - "삭제된 댓글입니다" 표시
  - 대댓글 구조 유지

#### N+1 문제 방지
- **Eager Loading:** `joinedload()` 사용
  - 목록: `joinedload(Board.author)`
  - 상세: `joinedload(Board.images)`
- **서브쿼리:** 좋아요/댓글 개수
  - 별도 쿼리로 집계

---

## ⚠️ 남아 있는 문제/리스크

### 1. Elasticsearch 미활용
- **현상:** 컨테이너는 실행 중이나 검색 기능 미구현
- **원인:** Logstash 파이프라인 미설정, FastAPI 연동 코드 부재
- **해결 계획:** s007 단계에서 게시글 검색 통합 (elasticsearch-py 사용)

### 2. 에러 처리 미흡
- **문제:**
  - 전역 예외 핸들러 부재
  - 프론트엔드 에러 메시지 UX 개선 필요
  - Oracle 연결 실패 시 재시도 로직 없음
- **해결 계획:**
  - FastAPI의 `@app.exception_handler` 구현
  - 프론트: 에러 모달 또는 토스트 메시지
  - DB 연결: sqlalchemy.pool.Pool retry 설정

### 3. 보안 강화 필요
- **현재 상태:**
  - CORS: 모든 origin 허용 (개발용)
  - Rate Limiting 미구현
  - HTTPS 미설정
- **해결 계획:**
  - CORS: 프로덕션에서 특정 도메인만 허용
  - slowapi를 이용한 Rate Limiting
  - Nginx + Let's Encrypt로 HTTPS 설정

### 4. 테스트 부재
- **문제:** 단위/통합 테스트 없음
- **해결 계획:**
  - pytest + pytest-asyncio
  - httpx.AsyncClient로 API 테스트
  - DB 테스트: SQLAlchemy TestSession

### 5. 성능 최적화 미완료
- **문제:**
  - DB 인덱스 미설정
  - 쿼리 N+1 문제 가능성 (Lazy Loading)
  - 이미지 리사이징/압축 미구현
- **해결 계획:**
  - 인덱스: MEMBER_EMAIL, BOARD_CODE, MEMBER_NO 등
  - Eager Loading: `joinedload()` 사용
  - Pillow로 이미지 리사이징

### 6. Docker 환경 이슈
- **문제:**
  - Oracle 컨테이너 재시작 시 연결 대기 로직 필요
  - 환경 변수 우선순위 혼란 (.env vs docker-compose.yml)
- **해결:**
  - Health check 개선
  - `env_file: .env` 사용 (docker-compose.yml)

---

## 🚀 다음 작업 우선순위

### 우선순위 1: 자유게시판 CRUD 포팅 (s007) - 진행 중 (2/3 완료)

**✅ 완료된 단계:**
1. ✅ DB 테이블 생성 + SQLAlchemy 모델
2. ✅ Pydantic 스키마
3. ✅ 게시판 목록 조회 API + Frontend
4. ✅ 게시글 상세 조회 API + Frontend

**⏳ 다음 단계 (3단계):**
5. 게시글 작성 API + Frontend (이미지 업로드 포함)
6. 게시글 수정/삭제 API + Frontend
7. 댓글 CRUD API + Frontend
8. 좋아요 API + Frontend

**현재까지의 성과:**
- CRUD 패턴 정립 (목록 조회, 상세 조회)
- 페이징/정렬/검색 구현
- 반응형 UI 구현
- JWT 인증 통합

**남은 작업의 중요성:**
1. **파일 업로드 구현** → 이미지 다중 업로드 (최대 5장)
2. **댓글 시스템** → 대댓글 재귀 구조 처리
3. **좋아요 기능** → 실시간 토글 UX
4. **Elasticsearch 연동 준비** → 전문 검색 기능 기반

### 우선순위 2: Elasticsearch 검색 통합
- s007 완료 후 게시글 전문 검색 기능 추가

### 우선순위 3: AI 챗봇 통합
- OpenAI API 연동 (글 작성 도우미)

### 우선순위 4: 모니터링/로깅
- Logstash 파이프라인 설정
- Kibana 대시보드 구성

---

## 📝 개발 워크플로우

### 코드 수정 시 재시작 필요 여부

| 변경 사항 | 재시작 필요? | 명령어 |
|-----------|-------------|--------|
| Python 코드 (.py) | ❌ 불필요 | 자동 리로드 (uvicorn --reload) |
| Static 파일 (HTML/CSS/JS) | ❌ 불필요 | 브라우저 새로고침 (Ctrl+Shift+R) |
| .env 파일 | ⚠️ restart만 | `docker-compose restart fastapi-backend` |
| requirements.txt | ✅ 필요 | `docker-compose build --no-cache fastapi-backend && docker-compose up -d` |
| Dockerfile | ✅ 필요 | `docker-compose down && docker-compose build --no-cache && docker-compose up -d` |
| docker-compose.yml | ✅ 필요 | `docker-compose down && docker-compose up -d` |

### 개발 시작 절차
```bash
# 1. 컨테이너 시작
docker-compose up -d

# 2. 로그 확인 (터미널 1)
docker-compose logs -f fastapi-backend

# 3. 코드 수정 (VS Code 또는 nano)
# → 저장 → 로그에서 "Reloading..." 확인

# 4. API 테스트 (터미널 2)
curl http://localhost:8000/health

# 5. 브라우저 테스트
# F12 → Network 탭 → 요청 확인

# 6. 작업 종료
docker-compose down
```

---

## 📚 참고 문서

### 프로젝트 히스토리
- `docs/adr/s001_loginSignUp_Prompt.md` - 로그인/회원가입 포팅
- `docs/adr/s002_kakaoLogin_Prompt.md` - 카카오 소셜 로그인 포팅
- `docs/adr/s003_Answer_loginSignUp_kakaoLogin.md` - s001~s002 통합 결과
- `docs/adr/s007_freeboard_Prompt.md` - 자유게시판 포팅 계획
- `s007_step1_report.md` - 자유게시판 1단계 (DB + 백엔드 API) 완료
- `s007_step2_report.md` - 자유게시판 2단계 (프론트엔드) 완료

### 주요 파일 위치

**Backend (자유게시판):**
- `models_freeboard.py` - SQLAlchemy 모델
- `board_schemas.py` - Pydantic 스키마
- `board_router.py` - FastAPI 라우터

**Frontend (자유게시판):**
- `/static/freeboardList.html/css/js` - 목록 화면
- `/static/freeboardDetail.html/css/js` - 상세 화면

**DB 초기화:**
- `/init_scripts/init_PDB_XEPDB1.sql` - 회원 테이블
- `init_freeboard.sql` - 게시판 테이블

**환경 설정:**
- `.env` - 환경 변수
- `docker-compose.yml` - Docker 설정

---

**작성자:** Claude (Anthropic)  
**프로젝트:** SpringBoot → FastAPI 포팅  
**버전:** 1.1 (s007 2단계 완료 반영)  
**최종 업데이트:** 2026년 1월 28일
