import streamlit as st
import pandas as pd
from datetime import datetime
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource

class SearchHistory:
    """
    Component for viewing and filtering search history with enhanced UI.
    """
    def __init__(self):
        self.db = SessionLocal()

    def render_filter_sidebar(self):
        """
        Render filters in sidebar and return filtered query conditions.
        (Note: Since this is meant to be integrated into main page or sidebar, 
        we can render local to where it's called, or assume st.sidebar context)
        """
        st.subheader("🔍 검색 필터")
        
        # Source Filter
        source_options = ["전체", "자동 수집", "수동 검색"]
        source_sel = st.pills("출처", source_options, default="전체")
        
        source_filter = None
        if source_sel == "자동 수집":
            source_filter = SearchSource.AUTO
        elif source_sel == "수동 검색":
            source_filter = SearchSource.MANUAL

        # Date Range Filter
        # Default to last 7 days
        today = datetime.now()
        start_date = st.date_input("시작 날짜", value=today.date())
        end_date = st.date_input("종료 날짜", value=today.date())

        # Keyword Search
        keyword_filter = st.text_input("키워드 검색", placeholder="키워드 입력...")

        return source_filter, start_date, end_date, keyword_filter

    def get_filtered_results(self, source, start_date, end_date, keyword):
        query = self.db.query(SearchResult).order_by(SearchResult.created_at.desc())

        if source:
            query = query.filter(SearchResult.source == source)
        
        if start_date:
            query = query.filter(SearchResult.created_at >= start_date)
        
        # End date + 1 day to include the end date fully
        if end_date:
            query = query.filter(SearchResult.created_at < pd.to_datetime(end_date) + pd.Timedelta(days=1))
            
        if keyword:
            query = query.filter(SearchResult.keyword.contains(keyword))
            
        return query.all()

    def render_history_dashboard(self):
        """
        Render the main history dashboard with filters and result cards.
        """
        # Top Filters
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
             source_options = ["전체", "Auto", "Manual"]
             source_sel = st.selectbox("Source", source_options, label_visibility="collapsed")
        
        with col2:
             # Simple date picking logic or just quick filters
             pass

        source_filter = None
        if source_sel == "Auto": source_filter = SearchSource.AUTO
        elif source_sel == "Manual": source_filter = SearchSource.MANUAL
        
        # Fetch Data
        results = self.get_filtered_results(source_filter, None, None, None)
        
        st.caption(f"총 {len(results)}건의 검색 기록이 있습니다.")

        # Display As Cards
        for res in results[:10]: # Limit to 10 for performance
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    tag = "🤖 [Auto]" if res.source == SearchSource.AUTO else "👤 [Manual]"
                    st.markdown(f"**{tag} {res.keyword}**")
                    st.caption(res.created_at.strftime("%Y-%m-%d %H:%M"))
                with c2:
                    if st.button("상세 보기", key=f"view_{res.id}"):
                         st.session_state.selected_key = res.search_key
                         st.session_state.current_mode = "history"
                         st.session_state.last_result = res
                         st.rerun()

                if res.ai_summary:
                    st.markdown(res.ai_summary[:100] + "..." if len(res.ai_summary) > 100 else res.ai_summary)

    def close(self):
        self.db.close()
