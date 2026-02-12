from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import pandas as pd
from .news_article import NewsArticle

@dataclass
class SearchResult:
    """
    뉴스 검색 한 세트의 결과를 나타내는 데이터 클래스.
    """
    search_key: str              # PK, "키워드-yyyymmddhhmm" 형식
    search_time: datetime         # 검색 실행 시간
    keyword: str                  # 검색 키워드
    articles: List[NewsArticle]   # 뉴스 기사 리스트
    ai_summary: str               # AI 요약 결과

    def to_dataframe(self) -> pd.DataFrame:
        """
        CSV 저장을 위해 Long format(기사 1건=1행)으로 변환
        """
        data = []
        for i, article in enumerate(self.articles, 1):
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "ai_summary": self.ai_summary
            })
        return pd.DataFrame(data)
