import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
import sys

from services.automation_service import AutomationService
from services.subscription_service import SubscriptionService
from services.report_service import ReportService
from database.session import SessionLocal, Base, engine
from domain.models import SearchResult, Subscription

class TestIntegrationPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create tables for testing
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # We might want to clean up, but using a file based db 
        # makes it persist. For real integration test we use it as is.
        pass

    def setUp(self):
        self.db = SessionLocal()
        # Clean up relevant tables before each test
        self.db.query(SearchResult).delete()
        self.db.query(Subscription).delete()
        self.db.commit()

        self.sub_service = SubscriptionService()
        self.auto_service = AutomationService()
        self.report_service = ReportService()

    def tearDown(self):
        self.db.close()

    @patch('services.automation_service.search_news')
    @patch('services.automation_service.summarize_news')
    @patch('services.report_service.generate_daily_insight')
    def test_full_pipeline(self, mock_insight, mock_summarize, mock_search):
        """
        Scenario: Subscription -> Auto Collection -> Report Generation -> PDF Export
        """
        # 1. Add Subscription
        keyword = "integration_test_coin"
        self.sub_service.add_subscription(keyword)
        
        # Verify subscription exists
        subs = self.sub_service.get_all_keywords()
        self.assertIn(keyword, subs)

        # 2. Run Automation Task
        # Mock external API calls - Search returns list of NewsArticle objects
        mock_article = MagicMock()
        mock_article.title = "Test Article Title"
        mock_article.url = "http://test.com/article"
        mock_article.snippet = "This is a snippet for integration test."
        mock_article.pub_date = "2023-01-01"
        mock_article.content = "Full content of the article."
        
        # search_news returns a list of articles
        mock_search.return_value = [mock_article]
        
        # summarize_news returns a string summary
        mock_summarize.return_value = f"AI Summary for {keyword}"
        
        # generate_daily_insight returns report content
        mock_insight.return_value = f"Insight Report for {keyword}"

        # Force update to ensure execution
        # We need to patch the internal calls inside AutomationService or ensure they work
        # Since we patched at module level, it should work.
        results = self.auto_service.run_automation_task(force_update=True)
        
        # Verify result was processed
        found = False
        target_key = ""
        # AutomationService returns a list of SearchResult objects
        if results:
            for r in results:
                if r.keyword == keyword:
                   found = True
                   target_key = r.search_key
                   break
        
        self.assertTrue(found, f"Keyword '{keyword}' should be processed by automation. Results: {results}")

        # Verify DB persistence
        # Re-query from DB to ensure it was saved
        db_result = self.db.query(SearchResult).filter(SearchResult.keyword == keyword).order_by(SearchResult.created_at.desc()).first()
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result.ai_summary, f"AI Summary for {keyword}")

        # 3. Generate Report
        # Generate custom report for this keyword
        # generate_custom_report calls generate_daily_insight internally, which is mocked
        report_content = self.report_service.generate_custom_report([target_key])
        
        self.assertIsNotNone(report_content)
        # Should contain the mocked insight return value
        self.assertIn(f"Insight Report for {keyword}", report_content) 

        # 4. Generate PDF
        # PDF generation also uses generate_daily_insight
        pdf_bytes = self.report_service.generate_custom_pdf_report([target_key])
        
        self.assertIsNotNone(pdf_bytes)
        self.assertTrue(len(pdf_bytes) > 0)
        self.assertTrue(pdf_bytes.startswith(b'%PDF-'))
        
        print(f"\n[Integration Test] Full pipeline success for keyword: {keyword}")

if __name__ == '__main__':
    unittest.main()
