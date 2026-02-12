import streamlit as st
from datetime import datetime
from config.settings import settings
from repositories.search_repository import SearchRepository
from services.search_service import search_news
from services.ai_service import summarize_news
from domain.search_result import SearchResult
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, render_settings, render_info, 
    render_history_list, render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key

# 1. 페이지 설정
st.set_page_config(page_title="TrendTracker", layout="wide")

def init_session_state():
    """
    세션 상태 초기화
    """
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

def main():
    init_session_state()
    
    # 설정 에러 체크
    from config.settings import settings_error
    if settings_error:
        st.error(settings_error)
        st.stop()
        
    # 리포지토리 초기화
    repository = SearchRepository(settings.CSV_PATH)
    
    # --- 사이드바 영역 ---
    render_sidebar_header()
    num_results = render_settings()
    render_info()
    st.sidebar.divider()
    
    search_keys = repository.get_all_keys()
    selected_key = render_history_list(search_keys)
    
    # 기록 선택 시 로직 (모드 전환)
    if selected_key and selected_key != st.session_state.selected_key:
        st.session_state.selected_key = selected_key
        st.session_state.current_mode = "history"
        st.session_state.last_result = repository.find_by_key(selected_key)
        st.rerun()
        
    csv_data = repository.get_all_as_csv()
    render_download_button(csv_data, len(search_keys) == 0)
    
    # --- 메인 영역 ---
    st.title("📊 TrendTracker: 실시간 뉴스 트렌드 분석")
    
    # 검색 폼 렌더링
    new_keyword = render_search_form()
    
    # 검색 실행 로직
    if new_keyword:
        try:
            # 1. 뉴스 검색
            with show_loading(f"🔍 '{new_keyword}' 관련 뉴스를 검색하고 있습니다..."):
                articles = search_news(new_keyword, num_results)
            
            if not articles:
                st.info("검색 결과가 없습니다.")
                return

            # 2. AI 요약
            with show_loading("🤖 AI가 내용을 분석하고 요약하고 있습니다..."):
                summary = summarize_news(articles)
            
            # 3. 결과 객체 생성
            search_key = generate_search_key(new_keyword)
            result = SearchResult(
                search_key=search_key,
                search_time=datetime.now(),
                keyword=new_keyword,
                articles=articles,
                ai_summary=summary
            )
            
            # 4. 저장 및 상태 업데이트
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

    # 결과 표시 영역
    if st.session_state.last_result:
        result = st.session_state.last_result
        
        if st.session_state.current_mode == "history":
            st.success(f"📅 과거 검색 기록을 불러왔습니다: {result.search_key}")
        
        render_summary(result.keyword, result.ai_summary)
        render_news_list(result.articles)
    else:
        # 환영 메시지 및 사용 안내
        if not new_keyword:
            st.markdown("""
            ### 👋 반갑습니다!
            **TrendTracker**는 최신 뉴스 트렌드를 한눈에 파악할 수 있도록 도와주는 도구입니다.
            
            **시작하는 방법:**
            1. 상단 검색창에 **궁금한 키워드**(예: 생성형 AI, 전기차 트렌드)를 입력하세요.
            2. **'검색'** 버튼을 누르면 실시간 뉴스를 가져옵니다.
            3. AI가 기사들을 분석하여 핵심 내용을 **불릿 포인트로 요약**해드립니다.
            
            *왼쪽 사이드바에서 과거 기록을 조회하거나 검색 건수를 조절할 수 있습니다.*
            """)
            
            if not search_keys:
                st.info("💡 아직 검색 기록이 없습니다. 키워드를 입력해 첫 검색을 시작해보세요!")

if __name__ == "__main__":
    main()
