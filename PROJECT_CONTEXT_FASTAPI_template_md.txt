[PROJECT]
- 서비스 이름:
- 목적 / 핵심 기능:

[ENVIRONMENT]
- Python 버전:
- FastAPI 버전:
- Pydantic: v1 / v2
- 실행 방식: uvicorn / gunicorn / docker

[APP STRUCTURE]
- app/
  - main.py:
  - api/ (router 구조):
  - models/ (ORM):
  - schemas/ (Pydantic DTO):
  - services/:
  - templates/ (Jinja2):
  - static/:
- 의도한 디렉토리 규칙:

[ROUTING]
- HTML 라우트:
  - 예: GET /users/{id} → TemplateResponse
- API 라우트:
  - 예: GET /api/users/{id} → JSON
- router 분리 기준:

[TEMPLATES]
- 템플릿 엔진: Jinja2
- DTO 전달 방식: DTO 그대로 (json() 사용 안 함)
- 공통 layout / include 구조:

[SCHEMAS (DTO)]
- 주요 Pydantic 모델:
- response_model 사용 여부:
- model_dump / dict 사용 규칙:

[DB / ORM]
- DB 종류:
- ORM: SQLAlchemy / SQLModel / Tortoise
- Session 관리 방식:
- 트랜잭션 전략:

[DEPENDENCIES]
- Depends 사용 패턴:
- 인증 / 인가 방식:
- 공통 의존성:

[KEY DECISIONS]
- (날짜) 설계 결정 + 이유
- 예: HTML 응답에서는 DTO → TemplateResponse로 직접 전달

[ERROR HANDLING]
- HTTPException 사용 규칙:
- 전역 예외 처리 여부:
- 에러 페이지 처리 방식:

[CURRENT STATE]
- 구현 완료:
- 진행 중:
- 막힌 부분 / 질문:

[NEXT TODO]
- 바로 다음 작업 1:
- 바로 다음 작업 2:

[OPEN QUESTIONS]
- 아직 결론 안 난 설계:
- 리팩토링 예정 포인트:
