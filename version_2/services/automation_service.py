from datetime import datetime
import logging
from typing import List, Optional

from services.trend_service import TrendService
from services.search_service import search_news
from services.ai_service import summarize_news
from services.deduplication_service import DeduplicationService
from repositories.search_repository import SearchRepository
from domain.search_result import SearchResult
from services.reliability_service import ReliabilityService
from services.notification_service import NotificationService
from domain.additional_models import TrendReliability
from domain.models import SearchSource
from services.subscription_service import SubscriptionService
from utils.key_generator import generate_search_key
from database.session import SessionLocal

logger = logging.getLogger(__name__)

class AutomationService:
    def __init__(self):
        self.trend_service = TrendService()
        self.repository = SearchRepository()
        self.db = SessionLocal() # For deduplication service
        self.dedup_service = DeduplicationService(self.db)
        self.subscription_service = SubscriptionService()

    def run_automation_task(self, category: str = 'all', limit: int = 3) -> List[SearchResult]:
        """
        Runs the full automation pipeline:
        1. Fetch trends from Google
        2. Filter duplicates
        3. Search news (Tavily)
        4. Generate AI summary (Gemini)
        5. Save to DB
        """
    def run_automation_task(self, category: str = 'all', limit: int = 3, force_update: bool = False) -> List[SearchResult]:
        """
        Runs the full automation pipeline:
        1. Fetch trends from Google
        2. Filter duplicates
        3. Search news (Tavily)
        4. Generate AI summary (Gemini)
        5. Save to DB
        """
        results = []
        
        # 0. Fetch Subscribed Keywords (Priority)
        subscribed_keywords = self.subscription_service.get_all_keywords()
        logger.info(f"Processing {len(subscribed_keywords)} subscribed keywords.")
        
        # Combine sources: Subscriptions first, then Trends
        # We might want to limit total processing or just ensure subscriptions are always processed.
        # For now, let's process all subscriptions + (limit) trends.
        
        # 1. Fetch trends
        trend_keywords = self.trend_service.get_trending_keywords(category=category, limit=limit)
        logger.info(f"Fetched {len(trend_keywords)} trending keywords: {trend_keywords}")
        
        # Create a unique list, prioritizing subscriptions
        # We filter out timestamps or other metadata if present
        all_keywords = list(set(subscribed_keywords + trend_keywords))
        
        # If we want to strictly follow 'limit' for trends but always do subscriptions:
        # But the requirement says "prioritize".
        
        for keyword in all_keywords:
            try:
                # 2. Check duplicate
                if not force_update and self.dedup_service.is_duplicate(keyword):
                    logger.info(f"Skipping duplicate/recent keyword: {keyword}")
                    continue
                
                # 3. Search News
                articles = search_news(keyword, num_results=5)
                if not articles:
                    logger.warning(f"No news found for keyword: {keyword}")
                    continue

                # 4. AI Summary
                summary = summarize_news(articles)
                
                # 5. Create SearchResult object
                search_key = generate_search_key(keyword)
                result = SearchResult(
                    search_key=search_key,
                    search_time=datetime.now(),
                    keyword=keyword,
                    articles=articles,
                    ai_summary=summary,
                    source="auto"
                )
                
                # 6. Save
                if self.repository.save(result):
                    results.append(result)
                    logger.info(f"Successfully processed keyword: {keyword}")
                    
                    # 7. Reliability Check & Notification (Only if saved successfully)
                    try:
                        rel_service = ReliabilityService()
                        score = rel_service.calculate_reliability_score(keyword)
                        
                        if score >= 50.0: # 임계값
                            notif_service = NotificationService()
                            rel_obj = TrendReliability(
                                keyword=keyword,
                                total_score=score,
                                google_score=score*0.4,
                                news_score=score*0.3
                            )
                            notif_service.send_trend_alert(rel_obj)
                    except Exception as e:
                        logger.error(f"Notification/Reliability check failed: {e}")
                        
                else:
                    logger.error(f"Failed to save result for keyword: {keyword}")

            except Exception as e:
                logger.error(f"Error processing keyword '{keyword}': {e}")
                continue
            
        self.db.close()
            
        return results

    def process_manual_keyword(self, keyword: str) -> Optional[SearchResult]:
        """
        Process a manually entered keyword through the same pipeline.
        """
        db = SessionLocal()
        try:
            dedup = DeduplicationService(db)
            # Manual keywords might skip deduplication check if user explicitly requests?
            # Or check if identical result exists recently.
            # Let's check anyway to avoid wasting API calls.
            if dedup.is_duplicate(keyword, expiry_hours=1): # Shorter expiry for manual retry
                 logger.info(f"Recent result exists for manual keyword: {keyword}")
                 # Maybe return existing result? For now, proceed to re-search if user clicked.
                 pass

            articles = search_news(keyword, num_results=5)
            if not articles:
                return None

            summary = summarize_news(articles)
            search_key = generate_search_key(keyword)
            
            result = SearchResult(
                search_key=search_key,
                search_time=datetime.now(),
                keyword=keyword,
                articles=articles,
                ai_summary=summary
            )
            setattr(result, 'source', SearchSource.MANUAL.value)
            
            self.repository.save(result)
            return result
        except Exception as e:
            logger.error(f"Manual processing failed for '{keyword}': {e}")
            return None
        finally:
            db.close()
