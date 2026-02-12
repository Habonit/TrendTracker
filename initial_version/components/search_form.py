import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    검색어 입력 필드와 버튼을 렌더링합니다.
    유효한 입력이면 전처리된 키워드를 반환합니다.
    """
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            keyword_input = st.text_input(
                "검색어 입력",
                placeholder="관심 있는 뉴스 키워드를 입력하세요 (예: AI 트렌드)",
                label_visibility="collapsed"
            )
        with col2:
            search_button = st.button("검색", use_container_width=True)

        if search_button:
            processed_key = preprocess_keyword(keyword_input)
            if not processed_key:
                st.warning("검색어를 입력해주세요")
                return None
            return processed_key
            
    return None
