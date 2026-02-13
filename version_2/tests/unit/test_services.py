import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from services.trend_service import TrendService
from services.automation_service import AutomationService
from domain.search_result import SearchResult

class TestTrendService(unittest.TestCase):
    def setUp(self):
        self.trend_service = TrendService()

    def test_get_trending_keywords_empty(self):
        """구글 트렌드 연결 해제로 인해 빈 리스트가 반환되어야 함"""
        result = self.trend_service.get_trending_keywords()
        self.assertEqual(result, [])

    def test_get_interest_over_time_empty(self):
        """구글 트렌드 연결 해제로 인해 빈 DataFrame이 반환되어야 함"""
        result = self.trend_service.get_interest_over_time("test")
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertTrue(result.empty)

class TestAutomationService(unittest.TestCase):
    def setUp(self):
        self.automation_service = AutomationService()
        self.automation_service.repository = MagicMock()
        self.automation_service.dedup_service = MagicMock()
        self.automation_service.subscription_service = MagicMock()
        self.automation_service.trend_service = MagicMock()

    @patch('services.automation_service.search_news')
    @patch('services.automation_service.summarize_news')
    def test_run_automation_task_subscription_only(self, mock_summarize, mock_search):
        """구독 키워드만 처리되는지 확인"""
        # Mock Setup
        self.automation_service.subscription_service.get_all_keywords.return_value = ["bitcoin", "ai"]
        self.automation_service.trend_service = MagicMock() # Ensure trend service is mocked
        self.automation_service.trend_service.get_trending_keywords.return_value = [] 
        self.automation_service.dedup_service.is_duplicate.return_value = False
        
        mock_search.return_value = [MagicMock(), MagicMock()] # 2 articles found
        mock_summarize.return_value = "SummaryResult"
        self.automation_service.repository.save.return_value = True

        # Execute
        results = self.automation_service.run_automation_task(category='all', limit=0)

        # Assertions
        # Since we mocked search to return list of 2 articles
        # And we set up 2 keywords: bitcoin, ai
        # We expect 2 SearchResult objects
        self.assertEqual(len(results), 2)
        self.automation_service.subscription_service.get_all_keywords.assert_called_once()
        self.assertEqual(self.automation_service.repository.save.call_count, 2)

if __name__ == '__main__':
    unittest.main()
