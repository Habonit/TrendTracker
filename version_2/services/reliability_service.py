from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource
from domain.additional_models import TrendReliability, DailyTrendReport

class ReliabilityService:
    def __init__(self):
        pass

    def _check_naver_trends(self, keyword: str) -> float:
        """
        Check Naver DataLab or Search API for trend verification.
        Returns a score between 0 and 30.
        """
        # Placeholder for Naver API integration
        # In real implementation:
        # 1. Call Naver Search API
        # 2. Check if total_results > threshold or if it appears in DataLab
        try:
            # Simulated check logic
            return 0.0 
        except Exception:
            return 0.0

    def _check_twitter_trends(self, keyword: str) -> float:
        """
        Check Twitter/X API for social buzz.
        Returns a score between 0 and 20.
        """
        # Placeholder for Twitter API
        return 0.0

    def calculate_reliability_score(self, keyword: str) -> float:
        """
        다양한 소스를 기반으로 트렌드 신뢰도 점수(0~100)를 산출합니다.
        """
        score = 0.0
        
        # 1. Google Trends (이미 수집된 결과가 있는지 확인)
        db = SessionLocal()
        try:
            # 최근 24시간 내 수집 횟수
            recent_count = db.query(SearchResult).filter(
                SearchResult.keyword == keyword,
                SearchResult.created_at >= datetime.now() - timedelta(hours=24)
            ).count()
            
            # 수집 빈도가 높을수록 점수 상승 (최대 40점)
            score += min(recent_count * 10, 40)
            
            # 2. News Coverage (Database)
            latest_result = db.query(SearchResult).filter(
                SearchResult.keyword == keyword
            ).order_by(SearchResult.created_at.desc()).first()
            
            if latest_result and latest_result.articles:
                article_count = len(latest_result.articles)
                # Max 30 points for news coverage
                score += min(article_count * 5, 30)
                
            # 3. Cross Verification (External APIs)
            score += self._check_naver_trends(keyword) # Max 30
            score += self._check_twitter_trends(keyword) # Max 20 -- Total potential > 100, cap at 100 later
            
            # Cap at 100
            score = min(score, 100.0)
            
            # Basic floor
            score = max(score, 10.0)
            
            # Save score
            self._save_score(db, keyword, score)
            
            return score
        finally:
            db.close()

    def _save_score(self, db: Session, keyword: str, score: float):
        entry = TrendReliability(
            keyword=keyword,
            total_score=score,
            google_score=score * 0.4, # 임시 비율
            news_score=score * 0.3
        )
        db.add(entry)
        db.commit()
    
    def get_high_reliability_trends(self, limit=5, threshold=50.0):
        """신뢰도 점수가 높은 최신 트렌드를 반환합니다."""
        db = SessionLocal()
        try:
            results = (db.query(TrendReliability)
                       .filter(TrendReliability.total_score >= threshold)
                       .order_by(TrendReliability.created_at.desc())
                       .limit(limit)
                       .all())
            return results
        finally:
            db.close()
