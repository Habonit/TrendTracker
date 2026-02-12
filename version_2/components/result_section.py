import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """
    AI 요약 섹션을 렌더링합니다.
    """
    st.subheader(f"🔍 {title} - AI 트렌드 요약")
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """
    뉴스 기사 리스트를 expander 형식으로 렌더링합니다.
    """
    st.subheader("📰 관련 뉴스 기사")
    
    if not articles:
        st.write("표시할 뉴스 기사가 없습니다.")
        return

    for article in articles:
        # 제목 (발행일) 형식으로 expander 레이블 구성
        label = article.title
        if article.pub_date:
            label = f"{label} ({article.pub_date})"
            
        with st.expander(label):
            if article.pub_date:
                st.markdown(f"**📅 발행일:** {article.pub_date}")
            
            st.write(article.snippet)
            st.markdown(f"[🔗 기사 보기]({article.url})")
