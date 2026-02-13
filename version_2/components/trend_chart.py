import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict

def render_wordcloud(keywords: List[Dict[str, int]]):
    """
    Render a wordcloud from a list of keywords and their frequencies.
    keywords: [{'keyword': 'term', 'count': 10}, ...]
    """
    if not keywords:
        st.info("시각화할 데이터가 충분하지 않습니다.")
        return

    # Convert list of dicts to a single dict for wordcloud
    word_freq = {item['keyword']: item['count'] for item in keywords}

    wc = WordCloud(
        font_path='malgun.ttf', # Windows default Korean font, might need adjustment on other OS
        width=800, 
        height=400,
        background_color='white'
    ).generate_from_frequencies(word_freq)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def render_trend_line_chart(trend_data: pd.DataFrame):
    """
    Render a line chart showing trend changes over time.
    DataFrame should have 'time' and 'value' columns, optionally 'keyword'.
    """
    if trend_data.empty:
        st.info("표시할 트렌드 데이터가 없습니다.")
        return

    fig = px.line(
        trend_data, 
        x='time', 
        y='value', 
        color='keyword',
        title="키워드별 관심도 변화",
        labels={'time': '시간', 'value': '관심도 점수', 'keyword': '키워드'}
    )
    st.plotly_chart(fig, use_container_width=True)

def render_category_pie_chart(category_counts: Dict[str, int]):
    """
    Render a pie chart showing the distribution of keywords by category.
    """
    if not category_counts:
        return

    df = pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count'])
    
    fig = px.pie(
        df, 
        values='Count', 
        names='Category', 
        title="수집된 트렌드 카테고리 비율"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_rank_change_chart(rank_data: pd.DataFrame):
    """
    Render a line chart for rank changes over time.
    DataFrame: [time, keyword, rank]
    """
    if rank_data.empty:
        return

    # Invert rank for visualization (Rank 1 at top)
    fig = px.line(
        rank_data, 
        x='time', 
        y='rank', 
        color='keyword',
        title="시간대별 검색어 순위 변화",
        markers=True,
    )
    fig.update_yaxes(autorange="reversed") # Rank 1 is higher visually
    st.plotly_chart(fig, use_container_width=True)
