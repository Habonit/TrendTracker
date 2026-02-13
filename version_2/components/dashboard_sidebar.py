import streamlit as st
from services.monitoring_service import MonitoringService
from utils.scheduler_manager import SchedulerManager
from datetime import datetime
import time

def render_dashboard_sidebar():
    """Render the monitoring dashboard in the sidebar."""
    # Use st. inside the function, relying on the caller to set the context (e.g. with st.sidebar:)
    st.divider()
    st.subheader("🖥️ 시스템 모니터링")
    
    # Refresh button
    if st.button("🔄 상태 새로고침"):
        st.rerun()

    scheduler = SchedulerManager()
    monitor = MonitoringService()
    
    # 1. Scheduler Status
    job_info = scheduler.get_job_info()
    status_stats = monitor.get_scheduler_status()
    
    if job_info and job_info['is_running']:
        st.success(f"✅ 스케줄러 실행 중")
        
        # Next run time
        next_run = job_info['next_run_time']
        if next_run:
            diff = next_run - datetime.now(next_run.tzinfo)
            total_seconds = int(diff.total_seconds())
            if total_seconds > 0:
                mins, secs = divmod(total_seconds, 60)
                st.caption(f"⏳ 다음 실행까지: {mins}분 {secs}초")
            else:
                st.caption("🚀 실행 준비 중...")
        else:
            st.caption("📅 예정된 작업 없음")
    else:
        st.error("🛑 스케줄러 중지됨")

    # 2. Statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 실행", status_stats.get("total_runs", 0))
    with col2:
        failed = status_stats.get("failed_runs_24h", 0)
        st.metric("24시간 실패", failed, delta_color="inverse" if failed > 0 else "normal")

    # 3. Recent Logs Expander
    with st.expander("📝 최근 실행 로그", expanded=False):
        logs = monitor.get_logs(limit=5)
        if not logs:
            st.caption("로그 내역이 없습니다.")
        else:
            for log in logs:
                icon = "✅" if log['status'] == 'success' else "❌" if log['status'] == 'failed' else "🏃"
                time_str = log['start_time'].strftime("%H:%M")
                st.caption(f"{icon} [{time_str}] {log['job_name']}")
                if log['message']:
                    st.caption(f"└ {log['message']}")
                st.divider()

    # Manual Run Trigger (Optional, good for testing)
    # if st.sidebar.button("▶️ 즉시 실행 (테스트)"):
    #     # Trigger logic could go here
    #     pass
