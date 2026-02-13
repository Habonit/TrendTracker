# Phase 01: 데이터 아키텍처 및 수집 엔진 안정화 ⚙️

## 🎯 목표
기존의 불안정한 CSV 저장 방식을 SQLite 기반의 RDBMS로 전환하고, Google Trends 수집 시 발생할 수 있는 장애(Rate Limit 등)에 대비한 안정적인 엔진을 구축합니다.

## 🛠️ 주요 개발 작업

### 1. SQLite 데이터베이스 및 ORM 도입
- **파일 위치**: `database/session.py`, `domain/models.py` (신규)
- **주요 기능**:
  - `SQLAlchemy`를 활용한 데이터베이스 연결 및 세션 관리.
  - **스키마 확장**:
    - `source`: 데이터 출처 (`"auto"`, `"manual"`)
    - `hash`: 검색어 및 일시 기준 고유값 (중복 분석 방지용)
    - `expiry_time`: 데이터 유효 기간 (지나면 재수집/재분석 대상)
    - `raw_content`: 수집된 원본 데이터 및 AI 요약 결과 통합 저장.

### 2. Google Trends (`TrendService`) 안정화
- **파일 위치**: `services/trend_service.py`
- **주요 기능**:
  - **Exception Handling**: `pytrends` 호출 실패 시 즉시 중단이 아닌 지능형 대기(Exponential Backoff) 도입.
  - **Rate Limit 대응**: 수집 간 무작위 지연(Random Sleep) 추가로 차단 방지.
  - **Fallback 준비**: RSS 피드 등 대체 수집 소스 연동을 위한 인터페이스 추상화.

### 3. 중복 분석 방지 및 캐싱 엔진
- **파일 위치**: `services/deduplication_service.py` (신규)
- **주요 기능**:
  - 키워드 분석 요청 시 DB에서 동일 검색어의 유효한(`expiry_time` 내) 데이터가 있는지 확인.
  - 존재할 경우 LLM API를 호출하지 않고 기존 결과를 반환하여 성능 향상 및 비용 절감.

## ✅ 완료 기준
- 모든 데이터가 CSV가 아닌 SQLite DB에 정상적으로 CRUD(생성/읽기/수정/삭제) 되는가?
- 수집 실패 상황에서 시스템이 죽지 않고 로그를 남기며 재시도하는가?
- 동일 키워드 연속 요청 시 LLM 호출 없이 기존 DB 데이터를 즉시 반환하는가?

---
## 💡 구현 포인트 (데이터 모델 예시)
```python
class SearchResult(Base):
    __tablename__ = "search_results"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, index=True)
    content_hash = Column(String, unique=True) # 중복 체크용
    source = Column(String) # auto/manual
    created_at = Column(DateTime, default=func.now())
    expiry_time = Column(DateTime) # 데이터 신선도 체크
```
