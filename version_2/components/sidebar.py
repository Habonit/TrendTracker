import streamlit as st
from typing import List, Optional, Tuple
from datetime import datetime
from utils.scheduler_manager import SchedulerManager
from services.monitoring_service import MonitoringService
from services.subscription_service import SubscriptionService
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource

scheduler_manager = SchedulerManager()
monitoring_service = MonitoringService()
subscription_service = SubscriptionService()

def render_sidebar_header():
    """Render sidebar header and monitoring badge."""
    st.sidebar.title("TrendTracker 🚀")
    
    # Monitoring info simple badge
    status = monitoring_service.get_scheduler_status()
    active_jobs = status.get('active_jobs', 0)
    
    if active_jobs > 0:
         st.sidebar.markdown(f"🟢 **시스템 가동 중** (진행 중: {active_jobs})")
    else:
         st.sidebar.markdown("⚪ **대기 상태**")
         
    st.sidebar.divider()

def render_trend_settings() -> Tuple[str, int]:
    """Render trend collection settings."""
    st.sidebar.subheader("📊 트렌드 수집 설정")
    
    category_options = {
        "모든 카테고리": "all",
        "비즈니스/금융": "business",
        "엔터테인먼트": "entertainment",
        "건강": "health",
        "과학/기술": "sci_tech",
        "스포츠": "sports"
    }
    
    selected_cat_label = st.sidebar.selectbox(
        "카테고리 선택",
        options=list(category_options.keys()),
        index=1
    )
    category = category_options[selected_cat_label]
    
    limit = st.sidebar.slider(
        "수집할 키워드 개수",
        min_value=1, 
        max_value=10, 
        value=3,
        help="한 번에 수집할 트렌드 키워드의 최대 개수입니다."
    )
    
    return category, limit

def render_scheduler_settings(automation_func, category, limit):
    """Render scheduler controls."""
    st.sidebar.subheader("⏰ 자동 실행 설정")
    
    interval_options = {
        "30초 (테스트)": 0.5,
        "10분": 10,
        "1시간": 60,
        "4시간": 240,
        "24시간": 1440
    }
    
    selected_interval = st.sidebar.selectbox(
        "실행 주기",
        options=list(interval_options.keys()),
        index=3 # default 4h
    )
    interval_minutes = interval_options[selected_interval]
    
    col1, col2 = st.sidebar.columns(2)
    start_btn = col1.button("🚀 시작", use_container_width=True)
    stop_btn = col2.button("🛑 중지", use_container_width=True)
    
    if start_btn:
        scheduler_manager.start()
        scheduler_manager.update_job(
            job_func=automation_func, 
            interval_minutes=interval_minutes,
            category=category,
            limit=limit,
            force_update=(interval_minutes == 0.5)  # Test mode forces update
        )
        st.toast("스케줄러가 시작되었습니다!", icon="✅")
        st.rerun()

    if stop_btn:
        scheduler_manager.shutdown()
        st.toast("스케줄러가 중지되었습니다.", icon="⏹️")
        st.rerun()
        
    job_info = scheduler_manager.get_job_info()
    if job_info and job_info.get("is_running"):
        next_run = job_info['next_run_time'].strftime("%H:%M:%S")
        st.sidebar.info(f"⏭️ 다음 실행: {next_run}")
        st.sidebar.success("✅ 스케줄러 실행 중")
    else:
        st.sidebar.warning("⏸️ 스케줄러 중지됨")

def render_subscription_manager():
    """Render pinned keyword management."""
    st.sidebar.divider()
    st.sidebar.subheader("📌 관심 키워드 구독")
    
    new_sub = st.sidebar.text_input("키워드 추가", placeholder="예: 비트코인")
    if st.sidebar.button("구독 추가"):
        if new_sub:
             if subscription_service.add_subscription(new_sub):
                 st.toast(f"'{new_sub}' 구독이 추가되었습니다.", icon="✅")
                 st.rerun()
             else:
                 st.error("구독 추가 실패")
    
    subs = subscription_service.get_subscriptions()
    if subs:
        st.sidebar.caption(f"구독 중인 키워드 ({len(subs)})")
        for sub in subs:
            c1, c2 = st.sidebar.columns([4, 1])
            c1.text(f"• {sub.keyword}")
            if c2.button("❌", key=f"del_sub_{sub.id}", help="구독 취소"):
                subscription_service.remove_subscription(sub.keyword)
                st.rerun()
    else:
        st.sidebar.caption("구독 중인 키워드가 없습니다.")

def render_history_list() -> Optional[str]:
    """Render search history list."""
    st.sidebar.divider()
    st.sidebar.subheader("📜 검색 기록 (최근 30건)")
    
    db = SessionLocal()
    try:
        results = (db.query(SearchResult.search_key, SearchResult.keyword, SearchResult.created_at, SearchResult.source)
                   .order_by(SearchResult.created_at.desc())
                   .limit(30)
                   .all())
        
        if not results:
            st.sidebar.info("저장된 검색 기록이 없습니다")
            return None
        
        display_options = []
        key_map = {}
        
        for res in results:
            icon = "📊" if res.source == SearchSource.AUTO else "✏️"
            source_tag = "[자동]" if res.source == SearchSource.AUTO else "[수동]"
            time_str = res.created_at.strftime("%m-%d %H:%M")
            display_name = f"{icon} {source_tag} {res.keyword} ({time_str})"
            display_options.append(display_name)
            key_map[display_name] = res.search_key
            
        selected_display = st.sidebar.selectbox(
            "기록 선택",
            options=["선택하세요..."] + display_options,
            label_visibility="collapsed"
        )
        
        if selected_display == "선택하세요...":
            return None
            
        return key_map.get(selected_display)
        
    finally:
        db.close()

def render_download_button(csv_data: str, is_empty: bool):
    """Render CSV download button."""
    st.sidebar.divider()
    filename = f"trendtracker_export_{datetime.now().strftime('%Y%m%d')}.csv"
    
    if is_empty or not csv_data:
        st.sidebar.button("📥 CSV 다운로드", disabled=True, help="저장된 데이터가 없습니다.")
    else:
        st.sidebar.download_button(
            label="📥 CSV 다운로드",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
