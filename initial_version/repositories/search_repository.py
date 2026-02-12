import os
import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
from domain.search_result import SearchResult
from domain.news_article import NewsArticle

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchRepository:
    """
    CSV 파일을 통해 뉴스 검색 결과를 관리하는 리포지토리 클래스
    """
    
    COLUMNS = [
        "search_key", "search_time", "keyword", "article_index",
        "title", "url", "snippet", "ai_summary"
    ]

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._ensure_directory()

    def _ensure_directory(self):
        """
        데이터 저장 폴더가 없으면 생성합니다.
        """
        directory = os.path.dirname(self.csv_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"데이터 디렉토리 생성 완료: {directory}")
            except Exception as e:
                logger.error(f"디렉토리 생성 실패: {e}")

    def load(self) -> pd.DataFrame:
        """
        CSV 파일을 로드합니다. 파일이 없으면 빈 DataFrame을 반환합니다.
        """
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=self.COLUMNS)
        
        try:
            df = pd.read_csv(self.csv_path)
            # 저장된 데이터의 컬럼이 일치하는지 확인 (간단한 검증)
            for col in self.COLUMNS:
                if col not in df.columns:
                    df[col] = None
            return df[self.COLUMNS]
        except Exception as e:
            logger.warning(f"CSV 로드 실패: {e}. 빈 데이터를 반환합니다.")
            return pd.DataFrame(columns=self.COLUMNS)

    def save(self, search_result: SearchResult) -> bool:
        """
        검색 결과를 CSV 파일에 추가 저장합니다.
        """
        try:
            new_df = search_result.to_dataframe()
            
            if os.path.exists(self.csv_path):
                # 기존 데이터에 추가
                existing_df = self.load()
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                updated_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            else:
                # 새 파일 생성
                new_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            
            logger.info(f"검색 결과 저장 완료: {search_result.search_key}")
            return True
        except Exception as e:
            logger.error(f"데이터 저장 중 에러 발생: {e}")
            return False

    def get_all_keys(self) -> List[str]:
        """
        중복 제거된 모든 search_key 리스트를 최신순으로 반환합니다.
        """
        df = self.load()
        if df.empty:
            return []
        
        # search_time을 기준으로 정렬 후 중복 제거된 키 추출
        try:
            # 시간 형식 변환 (문자열인 경우 대비)
            df['search_time'] = pd.to_datetime(df['search_time'])
            sorted_df = df.sort_values(by="search_time", ascending=False)
            keys = sorted_df['search_key'].unique().tolist()
            return keys
        except Exception as e:
            logger.error(f"키 목록 추출 실패: {e}")
            return df['search_key'].unique().tolist()

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """
        search_key로 검색 결과를 찾아 SearchResult 객체로 재구성합니다.
        """
        df = self.load()
        if df.empty:
            return None
        
        filtered_df = df[df['search_key'] == search_key]
        if filtered_df.empty:
            return None
        
        # 첫 번째 행에서 공통 정보 추출
        first_row = filtered_df.iloc[0]
        
        articles = []
        # 정렬하여 기사 순서 유지
        for _, row in filtered_df.sort_values(by="article_index").iterrows():
            articles.append(NewsArticle(
                title=str(row['title']),
                url=str(row['url']),
                snippet=str(row['snippet'])
            ))
        
        try:
            search_time = pd.to_datetime(first_row['search_time'])
        except:
            search_time = datetime.now()

        return SearchResult(
            search_key=str(first_row['search_key']),
            search_time=search_time,
            keyword=str(first_row['keyword']),
            articles=articles,
            ai_summary=str(first_row['ai_summary'])
        )

    def get_all_as_csv(self) -> str:
        """
        전체 데이터를 CSV 형식의 문자열로 반환합니다.
        """
        df = self.load()
        if df.empty:
            return ""
        return df.to_csv(index=False, encoding='utf-8-sig')
