import streamlit as st
from datetime import datetime
import pandas as pd
from config.settings import settings
from repositories.search_repository import SearchRepository
from services.search_service import search_news
from services.ai_service import summarize_news
from services.automation_service import AutomationService
from domain.search_result import SearchResult
from domain.models import SearchSource
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, 
    render_scheduler_settings,
    render_subscription_manager,
    render_history_list, 
    render_download_button,
    render_usage_guide
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from components.search_history import SearchHistory
from components.theme import inject_enterprise_theme, render_enterprise_header
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key
from database.init_db import init_db

# 1. 페이지 설정
st.set_page_config(
    page_title="TrendTracker",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_system():
    init_db()

def init_session_state():
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

def automation_task(force_update=False):
    """스케줄러에 의해 실행될 자동 수집 함수"""
    try:
        service = AutomationService()
        service.run_automation_task(category='all', limit=0, force_update=force_update)
    except Exception as e:
        print(f"Automation task error: {e}")

def main():
    init_system()
    init_session_state()
    
    # 설정 에러 체크
    from config.settings import settings_error
    if settings_error:
        st.error(settings_error)
        st.stop()
        
    repository = SearchRepository(settings.CSV_PATH)

    # ===== Enterprise Theme =====
    inject_enterprise_theme()

    # --- 사이드바 영역 ---
    with st.sidebar:
        render_sidebar_header()
        render_scheduler_settings(automation_task)
        render_subscription_manager()
        
        selected_key = render_history_list()
        
        df = repository.get_all_as_csv()
        csv_data = df.to_csv(index=False, encoding='utf-8-sig') 
        render_download_button(csv_data, len(df) == 0)
        
        render_usage_guide()

    # 기록 선택 시 로직
    if selected_key and selected_key != st.session_state.selected_key:
        st.session_state.selected_key = selected_key
        st.session_state.current_mode = "history"
        st.session_state.last_result = repository.find_by_key(selected_key)
        st.rerun()

    # ===== Main Content =====
    render_enterprise_header("TrendTracker", "AI 기반 지능형 트렌드 분석 플랫폼")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["검색 이력 / 리포트", "트렌드 검색"])
    
    # Tab 1: Search History & Report
    with tab1:
        history_comp = SearchHistory()
        history_comp.render_history_dashboard()
        history_comp.close()

    # Tab 2: Manual Search
    with tab2:
        st.markdown("""
            <div style="margin-bottom:1.5rem;">
                <h3 style="margin:0;color:#fff;">키워드 검색</h3>
                <p style="color:#888;font-size:0.85rem;margin:4px 0 0 0;">
                    관심 키워드를 입력하면 AI가 관련 뉴스를 분석하고 요약합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)

        new_keyword = render_search_form()
        
        if new_keyword:
            try:
                with show_loading(f"🔍 '{new_keyword}' 관련 뉴스를 검색하고 있습니다..."):
                    articles = search_news(new_keyword, num_results=5)
                
                if not articles:
                    st.info("검색 결과가 없습니다.")
                    return

                with show_loading("🤖 AI가 내용을 분석하고 요약하고 있습니다..."):
                    summary = summarize_news(articles)
                
                search_key = generate_search_key(new_keyword)
                result = SearchResult(
                    search_key=search_key,
                    search_time=datetime.now(),
                    keyword=new_keyword,
                    articles=articles,
                    ai_summary=summary,
                    source=SearchSource.MANUAL.value
                )
                
                with show_loading("💾 결과를 저장하고 있습니다..."):
                    if repository.save(result):
                        st.session_state.current_mode = "new_search"
                        st.session_state.last_result = result
                        st.session_state.selected_key = search_key
                        st.success(f"'{new_keyword}' 검색 완료! {len(articles)}건의 뉴스를 찾았습니다.")
                    else:
                        st.error("데이터 저장에 실패했습니다.")
                    
            except AppError as e:
                handle_error(e.error_type)
            except Exception as e:
                st.error(f"예기치 못한 오류가 발생했습니다: {str(e)}")

        # 결과 표시
        if st.session_state.last_result:
            result = st.session_state.last_result
            
            if st.session_state.current_mode == "history":
                pass
            
            st.divider()
            render_summary(result.keyword, result.ai_summary)
            render_news_list(result.articles)

if __name__ == "__main__":
    main()
