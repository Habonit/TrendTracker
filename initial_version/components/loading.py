import streamlit as st
from contextlib import contextmanager

@contextmanager
def show_loading(message: str = "뉴스를 검색하고 있습니다..."):
    """
    st.spinner를 context manager로 래핑하여 사용하기 편하게 구현합니다.
    """
    with st.spinner(message):
        yield
