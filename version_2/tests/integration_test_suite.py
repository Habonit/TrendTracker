
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.models import SearchResult, SearchSource, NewsArticle
from domain.additional_models import TrendReliability
from services.deduplication_service import DeduplicationService
from services.monitoring_service import MonitoringService
from services.subscription_service import SubscriptionService
from services.trend_service import TrendService
from services.reliability_service import ReliabilityService
from services.report_service import ReportService
from services.notification_service import NotificationService
from repositories.search_repository import SearchRepository
from database.session import SessionLocal

class TestIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    # --- Phase 1: Data Architecture & Collection ---
    def test_deduplication_service(self):
        # Setup
        mock_db = MagicMock()
        service = DeduplicationService(mock_db)
        
        # Scenario: Keyword exists and is not expired
        mock_result = MagicMock()
        mock_result.expiry_time = datetime(2099, 1, 1) # Future date
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_result
        
        self.assertTrue(service.is_duplicate("test_keyword"))
        
        # Scenario: Keyword does not exist
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
        self.assertFalse(service.is_duplicate("new_keyword"))

    def test_trend_service_fetch(self):
        # Setup
        service = TrendService()
        
        # Test that trending keywords return empty list (disabled feature)
        trends = service.get_trending_keywords(category='all', limit=2)
        self.assertEqual(trends, [])

    # --- Phase 2: Monitoring & Scheduler ---
    @patch('services.monitoring_service.SessionLocal')
    def test_monitoring_service_log(self, MockSession):
        # Setup
        mock_db = MockSession.return_value
        service = MonitoringService()
        
        # Test logging start
        log_id = service.log_job_start("test_job")
        
        # Verify DB interaction
        self.assertTrue(mock_db.add.called)
        self.assertTrue(mock_db.commit.called)
        
        # Test logging completion (mocking lookup)
        mock_log_entry = MagicMock()
        mock_log_entry.start_time = datetime.now() - timedelta(seconds=5) # Real datetime object
        
        # Filter chain for find log
        mock_db.query.return_value.filter.return_value.first.return_value = mock_log_entry
        # Fallback chain
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_log_entry

        service.log_job_completion("test_job", success=True)
        self.assertEqual(mock_log_entry.status, "success")

    # --- Phase 3: Hybrid UX (Subscription & Analytics) ---
    @patch('services.subscription_service.SessionLocal')
    def test_subscription_service(self, MockSession):
        mock_db = MockSession.return_value
        service = SubscriptionService()
        
        # Test adding subscription
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = service.add_subscription("bitcoin")
        self.assertTrue(result)
        self.assertTrue(mock_db.add.called)

    def test_trend_analytics(self):
        service = TrendService()
        
        # Test that interest over time returns empty DataFrame (disabled feature)
        result = service.get_interest_over_time("bitcoin")
        
        self.assertTrue(result.empty)

    # --- Phase 4: Intelligence & Reliability ---
    @patch('services.reliability_service.SessionLocal')
    def test_reliability_service(self, MockSession):
        mock_db = MockSession.return_value
        service = ReliabilityService()
        
        # Mock search result with articles
        mock_search_result = MagicMock()
        mock_search_result.articles = [MagicMock(), MagicMock(), MagicMock()] # 3 articles
        
        # DB query setup
        # 1. recent count query -> return 5
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        
        # 2. latest result query -> return mock_search_result
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_search_result
        
        score = service.calculate_reliability_score("high_trend")
        
        # Expectation: 
        # freq score: 5 * 10 = 50 -> capped at 40
        # news score: 3 * 5 = 15 -> capped at 30
        # Total = 40 + 15 = 55
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 55.0)
        self.assertLessEqual(score, 100.0)

    @patch('services.notification_service.requests')
    def test_notification_service(self, mock_requests):
        service = NotificationService()
        
        alert_data = TrendReliability(
            keyword="crisis",
            total_score=90.0,
            google_score=50.0,
            news_score=40.0
        )
        
        # Test sending alert
        service.send_trend_alert(alert_data)
        
        # Just verifying no exception is raised
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
