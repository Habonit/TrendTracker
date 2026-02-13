from sqlalchemy.orm import Session
from datetime import datetime
from domain.models import SearchResult
import hashlib

class DeduplicationService:
    def __init__(self, db: Session):
        self.db = db

    def is_duplicate(self, keyword: str, expiry_hours: int = 24) -> bool:
        """
        Check if a valid (non-expired) search result exists for the keyword.
        """
        existing = self.get_valid_result(keyword)
        if existing:
            # Check expiry
            if existing.expiry_time and existing.expiry_time > datetime.now():
                return True
        return False

    def get_valid_result(self, keyword: str) -> SearchResult:
        """
        Retrieve the latest valid search result for the given keyword.
        """
        return self.db.query(SearchResult).filter(
            SearchResult.keyword == keyword,
            SearchResult.expiry_time > datetime.now()
        ).order_by(SearchResult.created_at.desc()).first()

    def generate_content_hash(self, content: str) -> str:
        """
        Generate a SHA-256 hash for content deduplication.
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
