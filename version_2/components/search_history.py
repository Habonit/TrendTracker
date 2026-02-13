import streamlit as st
import pandas as pd
from datetime import datetime
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource
from repositories.search_repository import SearchRepository
from components.result_section import render_summary, render_news_list

class SearchHistory:
    """
    Component for viewing and filtering search history with enhanced UI.
    Supports: filtering, detail view, deletion, and CSV export.
    """
    def __init__(self):
        self.db = SessionLocal()
        self.repo = SearchRepository()

    def get_filtered_results(self, source, start_date, end_date, keyword):
        query = self.db.query(SearchResult).order_by(SearchResult.created_at.desc())

        if source:
            query = query.filter(SearchResult.source == source)
        
        if start_date:
            query = query.filter(SearchResult.created_at >= start_date)
        
        if end_date:
            query = query.filter(SearchResult.created_at < pd.to_datetime(end_date) + pd.Timedelta(days=1))
            
        if keyword:
            query = query.filter(SearchResult.keyword.contains(keyword))
            
        return query.all()

    def render_history_dashboard(self):
        """
        Render the main history dashboard with filters, result table, 
        detail view, delete, and CSV export.
        """
        
        # --- Detail View Mode ---
        # If a detail view is requested, show it first with a back button
        if st.session_state.get("detail_view_key"):
            self._render_detail_view()
            return  # Don't show the table when in detail view
        
        # --- Filter Bar ---
        col_filter1, col_filter2 = st.columns([1, 3])
        with col_filter1:
            source_options = ["전체", "Auto", "Manual"]
            source_sel = st.selectbox("출처 필터", source_options, label_visibility="collapsed")
        with col_filter2:
            keyword_search = st.text_input("키워드 검색", placeholder="키워드로 필터링...", label_visibility="collapsed")

        source_filter = None
        if source_sel == "Auto":
            source_filter = SearchSource.AUTO
        elif source_sel == "Manual":
            source_filter = SearchSource.MANUAL
        
        # Fetch Data
        results = self.get_filtered_results(source_filter, None, None, keyword_search if keyword_search else None)
        
        if not results:
            st.info("검색 기록이 없습니다.")
            return
        
        st.caption(f"총 **{len(results)}건**의 검색 기록 | 항목을 체크하여 상세 보기, 삭제, 리포트 생성이 가능합니다.")

        # --- Data Editor with Checkboxes ---
        data = []
        for res in results:
            data.append({
                "선택": False,
                "Key": res.search_key,
                "날짜": res.created_at.strftime("%Y-%m-%d %H:%M"),
                "출처": "🤖 Auto" if res.source == SearchSource.AUTO else "👤 Manual",
                "키워드": res.keyword,
                "요약": (res.ai_summary[:60] + "...") if res.ai_summary else "—"
            })
        
        df = pd.DataFrame(data)
        
        edited_df = st.data_editor(
            df,
            column_config={
                "선택": st.column_config.CheckboxColumn(
                    "선택",
                    help="작업할 항목을 선택하세요",
                    default=False,
                ),
                "Key": None,  # Hidden
            },
            hide_index=True,
            use_container_width=True,
            key="history_editor"
        )

        selected_rows = edited_df[edited_df["선택"]]
        selected_count = len(selected_rows)

        # --- Action Buttons ---
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if selected_count == 1:
                if st.button("View Details", use_container_width=True):
                    key = selected_rows.iloc[0]["Key"]
                    st.session_state.detail_view_key = key
                    st.rerun()
            else:
                st.button("View Details", disabled=True, use_container_width=True, 
                          help="1개 항목만 선택하세요" if selected_count > 1 else "항목을 선택하세요")

        with col_b:
            if selected_count > 0:
                if st.button(f"Delete ({selected_count})", use_container_width=True, type="primary"):
                    selected_keys = selected_rows["Key"].tolist()
                    deleted = self.repo.delete_by_keys(selected_keys)
                    if deleted > 0:
                        st.success(f"{deleted}건의 이력이 삭제되었습니다.")
                        st.rerun()
                    else:
                        st.error("삭제에 실패했습니다.")
            else:
                st.button("Delete", disabled=True, use_container_width=True)

        with col_c:
            if selected_count > 0:
                selected_keys = selected_rows["Key"].tolist()
                csv_data = self.repo.get_selected_as_csv(selected_keys)
                st.download_button(
                    label=f"Export CSV ({selected_count})",
                    data=csv_data,
                    file_name=f"selected_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("Export CSV", disabled=True, use_container_width=True)

    def _render_detail_view(self):
        """
        Render detail view for a selected search result.
        Shows AI summary and news articles inline.
        """
        key = st.session_state.detail_view_key
        
        # Back button
        if st.button("Back to list"):
            st.session_state.detail_view_key = None
            st.rerun()
        
        # Fetch full result via repository (avoids DetachedInstanceError)
        full_result = self.repo.find_by_key(key)
        
        if not full_result:
            st.error("해당 검색 결과를 찾을 수 없습니다.")
            return
        
        st.divider()
        
        # Header
        st.subheader(full_result.keyword)
        st.caption(f"검색 시간: {full_result.search_time.strftime('%Y-%m-%d %H:%M')}")
        
        # AI Summary
        render_summary(full_result.keyword, full_result.ai_summary)
        
        # News Articles
        render_news_list(full_result.articles)

    def close(self):
        self.db.close()
