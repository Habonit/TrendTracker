# TrendTracker 발전 로드맵 (Development Roadmap) 🚀

이 문서는 TrendTracker의 현재 기능을 바탕으로, 안정적인 자동 트렌드 수집 및 지능형 뉴스 분석 시스템으로 진화하기 위한 단계별 발전 계획을 담고 있습니다.

---

## 📅 프로젝트 개요
- **현재 버전 (v2.0)**: 수동 키워드 입력 기반 뉴스 수집 및 AI 요약 웹 앱
- **목표**: 데이터 안정성과 비용 효율성을 확보한 실시간 자동 트렌드 분석 플랫폼

---

## 🛠️ 핵심 개선 전략 (Core Strategy)

### 1. 데이터 아키텍처 현대화 (Storage Evolution)
- **Problem**: CSV 파일은 동시성 제어(Concurrency Control)가 불가능하여 자동화 환경에서 데이터 오염 위험이 큼.
- **Solution**: **SQLite 기반 RDBMS 도입**. 트랜잭션을 통한 데이터 무결성 확보 및 성능 최적화.

### 2. 수집 엔진 안정성 확보 (Robust Collection)
- **Problem**: Google Trends(pytrends)의 비공식 API는 Rate Limit 및 수동 차단에 취약함.
- **Solution**: **지능형 재시도(Backoff)** 로직 및 **멀티 소스(RSS, 네이버 등)** Fallback 체계 구축.

### 3. 지능형 중복 제거 및 비용 최적화 (Efficiency)
- **Problem**: 동일한 트렌드에 대해 반복적으로 LLM 분석을 수행하여 토큰 및 리소스 낭비.
- **Solution**: 데이터 해싱(Hashing) 및 유효 기간(TTL) 설정을 통한 **중복 분석 방지 엔진** 도입.

---

## 🚀 단계별 로드맵 (Phases)

### Phase 1: 데이터 기반 및 수집 안정화 (Foundation)
- [ ] **DB 전환**: CSV 저장소 구조를 SQLite 기반으로 마이그레이션 (`SQLAlchemy` 활용)
- [ ] **TrendService 고도화**: `pytrends` 예외 처리 및 수집 간격 최적화
- [ ] **데이터 스키마 확장**: `source`, `expiry_time`, `hash` 필드 추가로 데이터 추적성 확보
- [ ] **중복 방지 엔진**: 이미 수집/분석된 키워드에 대한 필터링 로직 구현

### Phase 2: 안정적인 백그라운드 엔진 (Execution)
- [ ] **Singleton 스케줄러**: Streamlit의 Re-run 환경에서도 안전한 단일 스케줄러 인스턴스 보장
- [ ] **상태 관리 대시보드**: 시스템 가동 상태, 마지막 수집 결과, 에러 로그 실시간 모니터링
- [ ] **에러 핸들링**: 수집 실패 시 알림 및 자동 복구 로직 강화

### Phase 3: 하이브리드 UX 및 시각화 (User Experience)
- [ ] **구독/관심 키워드 관리**: 사용자 관심 검색어 고정 및 우선 분석 기능
- [ ] **트렌드 타임라인**: 키워드 순위 및 관심도 변화를 시각적으로 추적하는 차트 추가
- [ ] **통합 검색 필터**: 자동 수집과 수동 입력을 아우르는 강력한 필터링 대시보드

### Phase 4: 지능형 인사이트 및 전달 (Intelligence)
- [ ] **다중 소스 교차 검증**: 다양한 채널의 데이터를 결합한 '트렌드 신뢰도 점수' 산출
- [ ] **일간 요약 리포트**: 24시간 트렌드를 종합 요약하여 인사이트 제공
- [ ] **외부 알림 연동**: 중요 트렌드 급상승 시 Slack/Telegram 실시간 푸시 알림

---

## 💡 기술 스택 확장 (Proposed Stack)
- **Database**: `SQLite` + `SQLAlchemy` (ORM)
- **Scheduling**: `APScheduler` (Background Process)
- **Resilience**: `Tenacity` (Advanced Retry Library)
- **Logging**: `Loguru` (Structured Logging)
- **Visualization**: `Plotly` or `Streamlit Charts`
