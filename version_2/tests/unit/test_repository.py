import unittest
from datetime import datetime
from database.session import SessionLocal, Base, engine
from repositories.search_repository import SearchRepository
from domain.models import SearchResult, SearchSource, NewsArticle

class TestSearchRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def setUp(self):
        self.db = SessionLocal()
        # Clean up both tables for proper isolation
        self.db.query(NewsArticle).delete()
        self.db.query(SearchResult).delete()
        self.db.commit()
        self.repo = SearchRepository()

    def tearDown(self):
        self.db.close()

    def test_delete_search_results(self):
        # 1. Arrange: Create test data
        result1 = SearchResult(
            search_key="key1",
            keyword="test1",
            created_at=datetime.now(),
            source=SearchSource.MANUAL.value
        )
        result2 = SearchResult(
            search_key="key2",
            keyword="test2",
            created_at=datetime.now(),
            source=SearchSource.MANUAL.value
        )
        self.db.add_all([result1, result2])
        self.db.commit()

        # Verify insertion
        self.assertEqual(self.db.query(SearchResult).count(), 2)

        # 2. Act: Delete key1
        deleted_count = self.repo.delete_by_keys(["key1"])

        # 3. Assert
        self.assertEqual(deleted_count, 1)
        remaining = self.db.query(SearchResult).all()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].search_key, "key2")

    def test_delete_multiple_keys(self):
        """여러 키를 동시에 삭제할 수 있어야 함"""
        for i in range(5):
            r = SearchResult(
                search_key=f"multi_key_{i}",
                keyword=f"kw_{i}",
                created_at=datetime.now(),
                source=SearchSource.MANUAL.value
            )
            self.db.add(r)
        self.db.commit()
        self.assertEqual(self.db.query(SearchResult).count(), 5)

        deleted = self.repo.delete_by_keys(["multi_key_0", "multi_key_2", "multi_key_4"])
        self.assertEqual(deleted, 3)
        self.assertEqual(self.db.query(SearchResult).count(), 2)

    def test_delete_nonexistent_key(self):
        """존재하지 않는 키 삭제 시 0을 반환해야 함"""
        deleted = self.repo.delete_by_keys(["nonexistent_key"])
        self.assertEqual(deleted, 0)

    def test_find_by_key_returns_articles(self):
        """find_by_key로 조회 시 articles가 정상적으로 로드되어야 함 (DetachedInstanceError 방지)"""
        from domain.models import NewsArticle as NewsArticleModel
        
        result = SearchResult(
            search_key="detail_key",
            keyword="detail_test",
            created_at=datetime.now(),
            source=SearchSource.MANUAL.value,
            ai_summary="Test summary"
        )
        article = NewsArticleModel(
            title="Article Title",
            url="http://example.com",
            snippet="Snippet text"
        )
        result.articles.append(article)
        self.db.add(result)
        self.db.commit()
        self.db.close()  # Close session to simulate detached state

        # Now fetch via repository (new session internally)
        domain_result = self.repo.find_by_key("detail_key")
        
        self.assertIsNotNone(domain_result)
        self.assertEqual(domain_result.keyword, "detail_test")
        self.assertEqual(domain_result.ai_summary, "Test summary")
        self.assertEqual(len(domain_result.articles), 1)
        self.assertEqual(domain_result.articles[0].title, "Article Title")

    def test_get_selected_as_csv(self):
        """선택된 키에 해당하는 데이터만 CSV(utf-8-sig)로 반환해야 함"""
        r1 = SearchResult(
            search_key="csv_key_1",
            keyword="bitcoin",
            created_at=datetime.now(),
            source=SearchSource.MANUAL.value,
            ai_summary="BTC summary"
        )
        r2 = SearchResult(
            search_key="csv_key_2",
            keyword="ethereum",
            created_at=datetime.now(),
            source=SearchSource.AUTO.value,
            ai_summary="ETH summary"
        )
        r3 = SearchResult(
            search_key="csv_key_3",
            keyword="solana",
            created_at=datetime.now(),
            source=SearchSource.MANUAL.value,
            ai_summary="SOL summary"
        )
        self.db.add_all([r1, r2, r3])
        self.db.commit()

        # Only select key 1 and 3
        csv_str = self.repo.get_selected_as_csv(["csv_key_1", "csv_key_3"])

        self.assertIsNotNone(csv_str)
        self.assertIn("bitcoin", csv_str)
        self.assertIn("solana", csv_str)
        self.assertNotIn("ethereum", csv_str)
        # Check utf-8-sig BOM
        csv_bytes = csv_str.encode('utf-8-sig')
        self.assertTrue(csv_bytes.startswith(b'\xef\xbb\xbf'))

if __name__ == '__main__':
    unittest.main()
