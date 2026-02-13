import streamlit as st
from datetime import datetime
import pandas as pd
from config.settings import settings
from repositories.search_repository import SearchRepository
from services.search_service import search_news
from services.ai_service import summarize_news
from services.automation_service import AutomationService
from services.report_service import ReportService
from services.trend_service import TrendService
from domain.search_result import SearchResult
from domain.models import SearchSource
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, 
    render_trend_settings, 
    render_scheduler_settings,
    render_subscription_manager,
    render_history_list, 
    render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from components.trend_chart import render_wordcloud, render_trend_line_chart, render_rank_change_chart
from components.search_history import SearchHistory
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key
from database.init_db import init_db

# 1. 페이지 설정
st.set_page_config(page_title="TrendTracker", layout="wide")

def init_system():
    # DB 초기화
    init_db()

def init_session_state():
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

def automation_task(category='all', limit=3, force_update=False):
    """
    스케줄러에 의해 실행될 자동 수집 함수
    """
    try:
        service = AutomationService()
        service.run_automation_task(category=category, limit=limit, force_update=force_update)
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

    # --- 사이드바 영역 ---
    with st.sidebar:
        render_sidebar_header()
        
        # 1. 트렌드 수집 설정
        category, limit = render_trend_settings()
        
        # 2. 스케줄러 설정
        render_scheduler_settings(automation_task, category, limit)
        
        # 3. 구독 관리 (신규)
        render_subscription_manager()
        
        st.divider()
        
        # 4. 검색 기록 (간편 이동)
        selected_key = render_history_list()
        
        # 데이터 내보내기
        # Fix: Ensure UTF-8 SIG for Excel
        df = repository.get_all_as_csv()
        csv_data = df.to_csv(index=False, encoding='utf-8-sig') 
        render_download_button(csv_data, len(df) == 0)

    # 기록 선택 시 로직
    if selected_key and selected_key != st.session_state.selected_key:
        st.session_state.selected_key = selected_key
        st.session_state.current_mode = "history"
        st.session_state.last_result = repository.find_by_key(selected_key)
        st.rerun()

    # --- 메인 영역 ---
    st.title("📊 TrendTracker: 지능형 트렌드 분석")
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["🚀 트렌드 대시보드", "📜 히스토리/필터", "🔍 수동 검색"])
    
    # Tab 1: Dashboard
    with tab1:
        st.markdown("### 실시간 트렌드 인사이트")
        
        # Fetch data for visualization
        # In a real app, this would be aggregated from DB
        # For now, let's gather from local repository/DB
        all_results = repository.get_all_results_obj()
        
        if not all_results:
            st.info("아직 수집된 데이터가 충분하지 않습니다.")
        else:
             # Prepare data for WordCloud
             # Simple frequency count of keywords
             keyword_counts = {}
             for r in all_results:
                 keyword_counts[r.keyword] = keyword_counts.get(r.keyword, 0) + 1
             
             wc_data = [{'keyword': k, 'count': v} for k, v in keyword_counts.items()]
             wc_data.sort(key=lambda x: x['count'], reverse=True)
             
             c1, c2 = st.columns([2, 1])
             with c1:
                 st.caption("🔥 핫 키워드 워드클라우드")
                 render_wordcloud(wc_data)
             with c2:
                 st.caption("📈 관심도 추이 (1개월)")
                 
                 top_keyword = wc_data[0]['keyword'] if wc_data else None
                 
                 if top_keyword:
                     try:
                         trend_service = TrendService()
                         # Fetch real data
                         # Use spinner
                         with st.spinner(f"'{top_keyword}' 트렌드 데이터 로딩 중..."):
                             trend_df = trend_service.get_interest_over_time(top_keyword)
                         
                         if not trend_df.empty and 'date' in trend_df.columns:
                             # Prepare for chart
                             # DataFrame has 'date' and 'keyword' column
                             trend_data = pd.DataFrame({
                                 'time': trend_df['date'],
                                 'value': trend_df[top_keyword],
                                 'keyword': top_keyword
                             })
                             render_trend_line_chart(trend_data)
                         else:
                             st.info(f"'{top_keyword}'에 대한 트렌드 데이터가 없습니다.")
                     except Exception as e:
                         st.error(f"트렌드 차트 로딩 실패: {e}")
                 else:
                     st.info("트렌드 데이터를 표시할 키워드가 없습니다.")

        st.divider()
        st.subheader("📑 일간 트렌드 리포트")
        
        report_service = ReportService()
        latest_report = report_service.get_latest_report()
        
        if latest_report:
            st.info(f"📅 작성일: {latest_report.created_at.strftime('%Y-%m-%d %H:%M')}")
            st.markdown(latest_report.content)
        else:
            st.info("아직 생성된 일간 리포트가 없습니다.")
        
        if st.button("📝 리포트 지금 생성하기"):
            with st.spinner("AI가 리포트를 작성 중입니다..."):
                content = report_service.generate_daily_report()
            if content:
                st.success("리포트가 생성되었습니다!")
                st.rerun()
            else:
                st.error("리포트 생성에 실패했습니다.")

    # Tab 2: Search History & Filter
    with tab2:
        history_comp = SearchHistory()
        history_comp.render_history_dashboard()
        history_comp.close()

    # Tab 3: Manual Search
    with tab3:
        # 검색 폼 렌더링
        new_keyword = render_search_form()
        
        # 검색 실행 로직
        if new_keyword:
            try:
                # 1. 뉴스 검색
                with show_loading(f"🔍 '{new_keyword}' 관련 뉴스를 검색하고 있습니다..."):
                    articles = search_news(new_keyword, num_results=5)
                
                if not articles:
                    st.info("검색 결과가 없습니다.")
                    return # Stop here

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
                    ai_summary=summary,
                    source=SearchSource.MANUAL.value
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

        # 결과 표시 (수동 검색 탭 하단)
        if st.session_state.last_result:
            result = st.session_state.last_result
            
            # 히스토리 모드일 때 메시지
            if st.session_state.current_mode == "history":
                tag = "[자동]" if getattr(result, 'source', 'manual') == 'auto' else "[수동]"
                st.success(f"📅 검색 기록 조회 중: {tag} {result.keyword}")
            
            render_summary(result.keyword, result.ai_summary)
            render_news_list(result.articles)

if __name__ == "__main__":
    main()
