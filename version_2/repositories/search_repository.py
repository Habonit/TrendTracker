from sqlalchemy.orm import Session
from database.session import SessionLocal
from domain.models import SearchResult as SearchResultModel, NewsArticle as NewsArticleModel, SearchSource
from domain.search_result import SearchResult
from domain.news_article import NewsArticle
from datetime import datetime
import pandas as pd
from typing import List, Optional

class SearchRepository:
    def __init__(self, csv_path: str = None):
        # csv_path는 하위 호환성을 위해 남겨두지만 실제로는 사용하지 않음 (또는 마이그레이션 용도)
        self.csv_path = csv_path

    def get_db(self):
        return SessionLocal()

    def save(self, result: SearchResult) -> bool:
        """
        도메인 객체(SearchResult)를 받아 DB에 저장합니다.
        """
        db = self.get_db()
        try:
            # 중복 체크 (search_key 기준)
            existing = db.query(SearchResultModel).filter(SearchResultModel.search_key == result.search_key).first()
            if existing:
                # 이미 존재하면 업데이트하거나 스킵 (여기서는 스킵 또는 에러 처리)
                # 현재 로직상 덮어쓰기보다는 새로 생성되는 구조임
                return True

            # 도메인 객체 -> ORM 모델 변환
            db_result = SearchResultModel(
                search_key=result.search_key,
                keyword=result.keyword,
                # source 필드는 도메인 객체에 없으면 default 'manual', 있으면 가져옴
                # 현재 도메인 객체에는 source가 없으므로 추후 추가 필요. 일단 'manual'로 가정하거나 kwargs 처리
                source=getattr(result, 'source', SearchSource.MANUAL.value),
                created_at=result.search_time,
                ai_summary=result.ai_summary
            )
            
            # 기사들 변환 및 추가
            for article in result.articles:
                db_article = NewsArticleModel(
                    title=article.title,
                    url=article.url,
                    snippet=article.snippet,
                    content=getattr(article, 'content', None) # 도메인 객체에 내용이 있다면
                )
                db_result.articles.append(db_article)
            
            db.add(db_result)
            db.commit()
            return True
        except Exception as e:
            print(f"Error saving to DB: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def get_all_keys(self) -> List[str]:
        """
        저장된 모든 검색 키(search_key) 리스트를 반환합니다.
        최신순 정렬.
        """
        db = self.get_db()
        try:
            results = db.query(SearchResultModel.search_key).order_by(SearchResultModel.created_at.desc()).all()
            return [r[0] for r in results]
        finally:
            db.close()

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """
        특정 키에 해당하는 검색 결과를 도메인 객체로 변환하여 반환합니다.
        """
        db = self.get_db()
        try:
            db_result = db.query(SearchResultModel).filter(SearchResultModel.search_key == search_key).first()
            if not db_result:
                return None
            
            # ORM -> 도메인 객체 변환
            articles = [
                NewsArticle(
                    title=a.title,
                    url=a.url,
                    snippet=a.snippet or "",
                    pub_date="" # DB에 저장 안했으면 빈값, 필요시 추가
                ) for a in db_result.articles
            ]
            
            return SearchResult(
                search_key=db_result.search_key,
                search_time=db_result.created_at,
                keyword=db_result.keyword,
                articles=articles,
                ai_summary=db_result.ai_summary or ""
            )
        finally:
            db.close()

    def get_all_as_csv(self) -> pd.DataFrame:
        """
        모든 데이터를 DataFrame으로 변환 (CSV export용)
        Long format: 기사 1건 = 1행
        """
        db = self.get_db()
        try:
            # Join query to get result info + article info
            results = db.query(SearchResultModel).order_by(SearchResultModel.created_at.desc()).all()
            
            data = []
            for res in results:
                for i, art in enumerate(res.articles, 1):
                    data.append({
                        "search_key": res.search_key,
                        "search_time": res.created_at,
                        "keyword": res.keyword,
                        "source": res.source, # 추가된 필드
                        "article_index": i,
                        "title": art.title,
                        "url": art.url,
                        "snippet": art.snippet,
                        "ai_summary": res.ai_summary
                    })
            
            return pd.DataFrame(data)
        finally:
            db.close()
    def get_all_results_obj(self, limit: int = 100) -> List[SearchResult]:
        """
        최근 검색 결과를 도메인 객체 리스트로 반환합니다.
        """
        db = self.get_db()
        try:
            db_results = db.query(SearchResultModel).order_by(SearchResultModel.created_at.desc()).limit(limit).all()
            
            results = []
            for db_res in db_results:
                articles = [
                    NewsArticle(
                        title=a.title,
                        url=a.url,
                        snippet=a.snippet or "",
                        pub_date=""
                    ) for a in db_res.articles
                ]
                
                # Handle source field safely
                params = {
                    "search_key": db_res.search_key,
                    "search_time": db_res.created_at,
                    "keyword": db_res.keyword,
                    "articles": articles,
                    "ai_summary": db_res.ai_summary or ""
                }
                
                # SearchResult dataclass might have 'source' field
                if hasattr(SearchResult, 'source'):
                    params['source'] = db_res.source
                
                results.append(SearchResult(**params))
                
            return results
        finally:
            db.close()

    def delete_by_keys(self, search_keys: List[str]) -> int:
        """
        주어진 search_key 리스트에 해당하는 검색 결과를 삭제합니다.
        cascade 설정에 의해 관련 articles도 함께 삭제됩니다.
        Returns: 삭제된 행 수
        """
        db = self.get_db()
        try:
            deleted = db.query(SearchResultModel).filter(
                SearchResultModel.search_key.in_(search_keys)
            ).delete(synchronize_session='fetch')
            db.commit()
            return deleted
        except Exception as e:
            print(f"Error deleting from DB: {e}")
            db.rollback()
            return 0
        finally:
            db.close()

    def get_selected_as_csv(self, search_keys: List[str]) -> str:
        """
        선택된 search_key들에 해당하는 데이터를 CSV 문자열로 반환합니다.
        인코딩: utf-8-sig (Excel 호환)
        """
        db = self.get_db()
        try:
            results = (db.query(SearchResultModel)
                       .filter(SearchResultModel.search_key.in_(search_keys))
                       .order_by(SearchResultModel.created_at.desc())
                       .all())
            
            data = []
            for res in results:
                if res.articles:
                    for i, art in enumerate(res.articles, 1):
                        data.append({
                            "search_key": res.search_key,
                            "search_time": res.created_at,
                            "keyword": res.keyword,
                            "source": res.source,
                            "article_index": i,
                            "title": art.title,
                            "url": art.url,
                            "snippet": art.snippet,
                            "ai_summary": res.ai_summary
                        })
                else:
                    data.append({
                        "search_key": res.search_key,
                        "search_time": res.created_at,
                        "keyword": res.keyword,
                        "source": res.source,
                        "article_index": 0,
                        "title": "",
                        "url": "",
                        "snippet": "",
                        "ai_summary": res.ai_summary
                    })
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False, encoding='utf-8-sig')
        finally:
            db.close()
