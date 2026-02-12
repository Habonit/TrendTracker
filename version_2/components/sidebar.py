import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """
    사이드바 상단 제목과 소개문을 렌더링합니다.
    """
    st.sidebar.title("TrendTracker")
    st.sidebar.markdown("### 키워드로 뉴스를 검색하고 AI가 요약해드립니다")
    st.sidebar.divider()

def render_settings() -> int:
    """
    검색 관련 설정을 렌더링하고 선택된 검색 건수를 반환합니다.
    """
    st.sidebar.subheader("⚙️ 설정")
    num_results = st.sidebar.slider(
        "뉴스 검색 건수",
        min_value=1,
        max_value=10,
        value=5,
        help="한 번에 검색할 뉴스 기사의 개수를 설정합니다."
    )
    return num_results

def render_info():
    """
    사용법, API 한도, 데이터 저장 안내 등을 렌더링합니다.
    """
    with st.sidebar.expander("ℹ️ 사용법", expanded=False):
        st.markdown("""
        1. **키워드 입력**: 궁금한 주제를 입력하세요.
        2. **검색 및 분석**: '검색' 버튼을 클릭하면 뉴스를 찾고 AI가 요약합니다.
        3. **기록 확인**: 과거 검색 결과는 사이드바 하단에서 다시 볼 수 있습니다.
        4. **내보내기**: 전체 기록을 CSV로 다운로드할 수 있습니다.
        """)

    with st.sidebar.expander("📊 API 한도", expanded=False):
        st.info("Tavily 무료 플랜: 월 1,000건 검색 가능")
        st.info("Gemini API: 분당 요청 제한(RPM) 확인 필요")

    with st.sidebar.expander("💾 데이터 저장 안내", expanded=False):
        st.markdown("""
        - 검색 기록은 CSV 파일(`data/search_history.csv`)에 저장됩니다.
        - CSV 파일을 삭제하거나 경로를 변경하면 이전 검색 기록이 모두 사라집니다.
        - 중요한 기록은 CSV 다운로드 기능을 통해 백업해주세요.
        """)

def render_history_list(search_keys: List[str]) -> Optional[str]:
    """
    과거 검색 기록 목록을 렌더링하고 선택된 키를 반환합니다.
    """
    st.sidebar.subheader("📜 검색 기록")
    
    if not search_keys:
        st.sidebar.info("저장된 검색 기록이 없습니다")
        return None
    
    # "키워드 (yyyy-mm-dd HH:MM)" 형식으로 표시하기 위해 변환
    display_options = []
    key_map = {}
    
    for key in search_keys:
        try:
            # "키워드-yyyyMMddHHmm" 형식 분리
            parts = key.rsplit('-', 1)
            keyword = parts[0]
            timestamp_str = parts[1]
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
            display_name = f"{keyword} ({dt.strftime('%Y-%m-%d %H:%M')})"
        except:
            display_name = key
            
        display_options.append(display_name)
        key_map[display_name] = key
        
    selected_display = st.sidebar.selectbox(
        "과거 기록 불러오기",
        options=["선택하세요..."] + display_options,
        index=0,
        label_visibility="collapsed"
    )
    
    if selected_display == "선택하세요...":
        return None
        
    return key_map.get(selected_display)

def render_download_button(csv_data: str, is_empty: bool):
    """
    CSV 다운로드 버튼을 렌더링합니다.
    """
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
