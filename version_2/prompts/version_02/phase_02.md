# Phase 02: 안정적인 백그라운드 엔진 및 모니터링 ⏲️

## 🎯 목표
Streamlit의 특수한 실행 환경(Re-run)에서도 안정적으로 동작하는 단일 스케줄러 인스턴스를 구축하고, 시스템의 가동 상태를 실시간으로 모니터링할 수 있는 UI를 제공합니다.

## 🛠️ 주요 개발 작업

### 1. Singleton 백그라운드 스케줄러 구현
- **파일 위치**: `utils/scheduler_manager.py` (신규)
- **주요 기능**:
  - **Singleton Pattern**: 여러 세션에서 접속하더라도 단 하나의 `BackgroundScheduler`만 실행되도록 보장.
  - **Thread-safe Job Management**: 자동 수집 작업이 중복 실행되지 않도록 잠금(Lock) 메커니즘 적용.
  - **Dynamic Config**: UI에서 변경된 수집 주기(Interval)를 재시작 없이 즉시 반영.

### 2. 스케줄러 상태 및 에러 모니터링
- **파일 위치**: `services/monitoring_service.py` (신규)
- **주요 기능**:
  - **Heartbeat 기록**: 스케줄러가 정상 작동 중인지 주기적으로 DB에 상태 기록.
  - **실행 이력(Job Log) 추적**: 성공/실패 여부, 소요 시간, 실패 사유(Traceback)를 통합 로깅.
  - **에러 알림**: 연속 N회 실패 시 시스템 경고 플래그 활성화.

### 3. 모니터링 대시보드 UI
- **파일 위치**: `components/dashboard_sidebar.py` 또는 별도 탭
- **주요 기능**:
  - 리얼타임 상태 표시 (예: "시스템 정상 가공 중 ✅", "마지막 수집: 10분 전")
  - 다음 실행 예정 시간(`next_run_time`) 카운트다운 표시.
  - 최근 발생한 시스템 로그 및 에러 내역 요약 보기.

## ✅ 완료 기준
- 사용자가 페이지를 새로고침하거나 브라우저를 닫아도 스케줄러가 백그라운드에서 유지되는가?
- 스케줄러가 발생시킨 모든 에러가 로그 파일 및 DB에 누락 없이 기록되는가?
- 대시보드 상에서 스케줄러의 현재 상태를 한눈에 파악할 수 있는가?

---
## 💡 구현 포인트 (Singleton 스케줄러 예시)
```python
class SchedulerManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SchedulerManager, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
        return cls._instance
```
- Streamlit에서 `st.cache_resource`를 활용하여 싱글톤 인스턴스를 유지하는 방법도 검토 필요.
