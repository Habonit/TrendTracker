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
    """Premium sidebar header with gradient badge and animated status."""
    st.sidebar.markdown("""
        <style>
            @keyframes status-pulse {
                0%, 100% { opacity: 1; box-shadow: 0 0 4px rgba(52,211,153,0.4); }
                50% { opacity: 0.7; box-shadow: 0 0 10px rgba(52,211,153,0.7); }
            }
        </style>
        <div style="padding:0.4rem 0 0.6rem 0;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="
                    width:32px;height:32px;
                    background: linear-gradient(135deg, #2563EB, #7C3AED);
                    border-radius: 8px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow: 0 2px 10px rgba(37,99,235,0.35);
                ">
                    <div style="
                        width:12px;height:12px;
                        background:#fff;
                        clip-path: polygon(50% 8%, 95% 92%, 5% 92%);
                    "></div>
                </div>
                <div>
                    <span style="
                        font-size:1rem;font-weight:700;
                        color:#FFFFFF;letter-spacing:-0.02em;
                    ">TrendTracker</span>
                    <span style="
                        display:inline-block;margin-left:6px;
                        font-size:0.5rem;font-weight:700;
                        background: linear-gradient(135deg, #2563EB, #7C3AED);
                        color:#fff;
                        padding:2px 7px;border-radius:4px;
                        letter-spacing:0.06em;
                        box-shadow: 0 1px 4px rgba(99,102,241,0.3);
                    ">PRO</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    status = monitoring_service.get_scheduler_status()
    active_jobs = status.get('active_jobs', 0)

    if active_jobs > 0:
        st.sidebar.markdown(f"""
            <div style="display:flex;align-items:center;gap:7px;margin:0.4rem 0 0.3rem 0;">
                <div style="
                    width:7px;height:7px;border-radius:50%;
                    background:#34D399;
                    animation: status-pulse 2s ease-in-out infinite;
                "></div>
                <span style="color:#CBD5E1;font-size:0.72rem;">Active &middot; {active_jobs} job(s)</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
            <div style="display:flex;align-items:center;gap:7px;margin:0.4rem 0 0.3rem 0;">
                <div style="width:7px;height:7px;border-radius:50%;background:#475569;"></div>
                <span style="color:#94A3B8;font-size:0.72rem;">Idle</span>
            </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:0.5rem 0;">', unsafe_allow_html=True)


def render_scheduler_settings(automation_func):
    """Premium scheduler settings with glass cards."""
    st.sidebar.markdown("""
        <p style="color:#E2E8F0;font-size:0.75rem;font-weight:700;
            letter-spacing:0.05em;text-transform:uppercase;margin:0.6rem 0 0.15rem 0;">
            Scheduler
        </p>
        <p style="color:#94A3B8;font-size:0.68rem;margin:0 0 0.5rem 0;">
            구독 키워드 자동 수집 주기
        </p>
    """, unsafe_allow_html=True)

    interval_options = {
        "30s (test)": 0.5,
        "10 min": 10,
        "1 hour": 60,
        "4 hours": 240,
        "24 hours": 1440
    }

    selected_interval = st.sidebar.selectbox(
        "Interval",
        options=list(interval_options.keys()),
        index=3,
        label_visibility="collapsed"
    )
    interval_minutes = interval_options[selected_interval]

    col1, col2 = st.sidebar.columns(2)
    start_btn = col1.button("Start", use_container_width=True)
    stop_btn = col2.button("Stop", use_container_width=True)

    if start_btn:
        scheduler_manager.start()
        scheduler_manager.update_job(
            job_func=automation_func,
            interval_minutes=interval_minutes,
            force_update=(interval_minutes == 0.5)
        )
        st.toast("Scheduler started", icon="✅")
        st.rerun()

    if stop_btn:
        scheduler_manager.shutdown()
        st.toast("Scheduler stopped", icon="⏹")
        st.rerun()

    job_info = scheduler_manager.get_job_info()
    if job_info and job_info.get("is_running"):
        next_run = job_info['next_run_time'].strftime("%H:%M:%S")
        st.sidebar.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(52,211,153,0.08), rgba(6,182,212,0.06));
                border:1px solid rgba(52,211,153,0.2);
                border-radius:8px;
                padding:0.5rem 0.7rem;
                margin:0.3rem 0;
                display:flex;justify-content:space-between;align-items:center;
                backdrop-filter: blur(4px);
            ">
                <span style="color:#34D399;font-size:0.72rem;font-weight:600;">Running</span>
                <span style="color:#CBD5E1;font-size:0.68rem;">Next: {next_run}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
            <div style="
                background: rgba(255,255,255,0.02);
                border:1px solid rgba(255,255,255,0.06);
                border-radius:8px;
                padding:0.5rem 0.7rem;
                margin:0.3rem 0;
            ">
                <span style="color:#94A3B8;font-size:0.72rem;">Stopped</span>
            </div>
        """, unsafe_allow_html=True)


def render_subscription_manager():
    """Premium subscription manager with glass tags."""
    st.sidebar.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:0.7rem 0;">', unsafe_allow_html=True)
    st.sidebar.markdown("""
        <p style="color:#E2E8F0;font-size:0.75rem;font-weight:700;
            letter-spacing:0.05em;text-transform:uppercase;margin:0 0 0.15rem 0;">
            Subscriptions
        </p>
        <p style="color:#94A3B8;font-size:0.68rem;margin:0 0 0.4rem 0;">
            자동 수집 키워드 관리
        </p>
    """, unsafe_allow_html=True)

    col_input, col_btn = st.sidebar.columns([3, 1])
    with col_input:
        new_sub = st.text_input("Add keyword", placeholder="키워드 입력", label_visibility="collapsed")
    with col_btn:
        add_clicked = st.button("Add", use_container_width=True)

    if add_clicked and new_sub:
        if subscription_service.add_subscription(new_sub):
            st.toast(f"'{new_sub}' added", icon="✅")
            st.rerun()
        else:
            st.error("추가 실패")

    subs = subscription_service.get_subscriptions()
    if subs:
        for sub in subs:
            col_kw, col_del = st.sidebar.columns([5, 1])
            col_kw.markdown(f"""
                <div style="
                    display:inline-flex;align-items:center;gap:6px;
                    background: rgba(37,99,235,0.08);
                    border: 1px solid rgba(37,99,235,0.15);
                    border-radius: 6px;
                    padding: 0.25rem 0.6rem;
                    margin: 0.1rem 0;
                ">
                    <span style="color:#93C5FD;font-size:0.78rem;">{sub.keyword}</span>
                </div>
            """, unsafe_allow_html=True)
            if col_del.button("×", key=f"del_sub_{sub.id}", help=f"Remove '{sub.keyword}'"):
                subscription_service.remove_subscription(sub.keyword)
                st.rerun()
    else:
        st.sidebar.markdown("""
            <p style="color:#94A3B8;font-size:0.72rem;font-style:italic;margin:0.3rem 0;">
                No subscriptions
            </p>
        """, unsafe_allow_html=True)


def render_history_list() -> Optional[str]:
    """Premium history selector."""
    st.sidebar.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:0.7rem 0;">', unsafe_allow_html=True)
    st.sidebar.markdown("""
        <p style="color:#E2E8F0;font-size:0.75rem;font-weight:700;
            letter-spacing:0.05em;text-transform:uppercase;margin:0 0 0.15rem 0;">
            Recent History
        </p>
        <p style="color:#94A3B8;font-size:0.68rem;margin:0 0 0.4rem 0;">
            최근 30건 검색 기록
        </p>
    """, unsafe_allow_html=True)

    db = SessionLocal()
    try:
        results = (db.query(SearchResult.search_key, SearchResult.keyword, SearchResult.created_at, SearchResult.source)
                   .order_by(SearchResult.created_at.desc())
                   .limit(30)
                   .all())

        if not results:
            st.sidebar.markdown("""
                <p style="color:#94A3B8;font-size:0.72rem;font-style:italic;">No history</p>
            """, unsafe_allow_html=True)
            return None

        display_options = []
        key_map = {}

        for res in results:
            source_tag = "A" if res.source == SearchSource.AUTO else "M"
            time_str = res.created_at.strftime("%m/%d %H:%M")
            display_name = f"[{source_tag}] {res.keyword} · {time_str}"
            display_options.append(display_name)
            key_map[display_name] = res.search_key

        selected_display = st.sidebar.selectbox(
            "History",
            options=["Select..."] + display_options,
            label_visibility="collapsed"
        )

        if selected_display == "Select...":
            return None

        return key_map.get(selected_display)

    finally:
        db.close()


def render_download_button(csv_data: str, is_empty: bool):
    """Premium CSV export button (all data)."""
    st.sidebar.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:0.7rem 0;">', unsafe_allow_html=True)
    filename = f"trendtracker_all_{datetime.now().strftime('%Y%m%d')}.csv"

    if is_empty or not csv_data:
        st.sidebar.button("Export All (CSV)", disabled=True, use_container_width=True)
    else:
        st.sidebar.download_button(
            label="Export All (CSV)",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )


def render_usage_guide():
    """Premium guide with gradient cards for API limits."""
    st.sidebar.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:0.7rem 0;">', unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style="margin-bottom:1rem;">
            <p style="color:#E2E8F0;font-size:0.75rem;font-weight:700;
                letter-spacing:0.05em;text-transform:uppercase;margin:0 0 0.5rem 0;">
                Guide
            </p>
            <div style="color:#CBD5E1;font-size:0.7rem;line-height:1.9;">
                <div style="display:flex;gap:10px;margin-bottom:5px;align-items:flex-start;">
                    <span style="
                        background:linear-gradient(135deg, #2563EB, #7C3AED);
                        color:#fff;font-size:0.55rem;font-weight:700;
                        padding:2px 6px;border-radius:4px;min-width:20px;text-align:center;
                    ">1</span>
                    <span>키워드 입력 후 <span style="color:#E2E8F0;font-weight:500;">Search</span> 클릭</span>
                </div>
                <div style="display:flex;gap:10px;margin-bottom:5px;align-items:flex-start;">
                    <span style="
                        background:linear-gradient(135deg, #2563EB, #7C3AED);
                        color:#fff;font-size:0.55rem;font-weight:700;
                        padding:2px 6px;border-radius:4px;min-width:20px;text-align:center;
                    ">2</span>
                    <span>AI가 관련 뉴스를 분석하고 요약</span>
                </div>
                <div style="display:flex;gap:10px;margin-bottom:5px;align-items:flex-start;">
                    <span style="
                        background:linear-gradient(135deg, #2563EB, #7C3AED);
                        color:#fff;font-size:0.55rem;font-weight:700;
                        padding:2px 6px;border-radius:4px;min-width:20px;text-align:center;
                    ">3</span>
                    <span>이력 탭에서 체크 후 CSV 추출</span>
                </div>
                <div style="display:flex;gap:10px;align-items:flex-start;">
                    <span style="
                        background:linear-gradient(135deg, #2563EB, #7C3AED);
                        color:#fff;font-size:0.55rem;font-weight:700;
                        padding:2px 6px;border-radius:4px;min-width:20px;text-align:center;
                    ">4</span>
                    <span>전체 데이터는 Export All로 내보내기</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div>
            <p style="color:#E2E8F0;font-size:0.75rem;font-weight:700;
                letter-spacing:0.05em;text-transform:uppercase;margin:0 0 0.5rem 0;">
                API Limits
            </p>
            <div style="
                background: linear-gradient(135deg, rgba(37,99,235,0.06), rgba(124,58,237,0.04));
                border:1px solid rgba(37,99,235,0.12);
                border-radius:8px;
                padding:0.6rem 0.75rem;
                margin-bottom:0.4rem;
                backdrop-filter: blur(4px);
            ">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="color:#CBD5E1;font-size:0.7rem;">Tavily Search</span>
                    <span style="color:#CBD5E1;font-size:0.7rem;font-weight:600;">1,000 / mo</span>
                </div>
                <div style="width:100%;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;">
                    <div style="
                        width:25%;height:100%;
                        background: linear-gradient(90deg, #2563EB, #3B82F6);
                        border-radius:2px;
                        box-shadow: 0 0 6px rgba(37,99,235,0.4);
                    "></div>
                </div>
            </div>
            <div style="
                background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(37,99,235,0.04));
                border:1px solid rgba(124,58,237,0.12);
                border-radius:8px;
                padding:0.6rem 0.75rem;
                backdrop-filter: blur(4px);
            ">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="color:#CBD5E1;font-size:0.7rem;">Gemini API</span>
                    <span style="color:#CBD5E1;font-size:0.7rem;font-weight:600;">RPM 제한</span>
                </div>
                <div style="width:100%;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;">
                    <div style="
                        width:10%;height:100%;
                        background: linear-gradient(90deg, #7C3AED, #8B5CF6);
                        border-radius:2px;
                        box-shadow: 0 0 6px rgba(124,58,237,0.4);
                    "></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
