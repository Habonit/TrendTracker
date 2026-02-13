from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base
import enum

class SearchSource(str, enum.Enum):
    MANUAL = "manual"
    AUTO = "auto"

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    search_key = Column(String, index=True) # 기존 CSV와의 호환성을 위해 유지 (ex: keyword-YYYYMMDDHHMM)
    keyword = Column(String, index=True, nullable=False)
    source = Column(String, default=SearchSource.MANUAL.value) # auto/manual as string
    created_at = Column(DateTime, default=datetime.now)
    expiry_time = Column(DateTime, nullable=True) # 데이터 유효 기간
    content_hash = Column(String, unique=True, index=True, nullable=True) # 중복 분석 방지용 해시
    ai_summary = Column(Text, nullable=True)

    # Relationship
    articles = relationship("NewsArticle", back_populates="search_result", cascade="all, delete-orphan")

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey("search_results.id"))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    snippet = Column(Text, nullable=True)
    content = Column(Text, nullable=True) # 본문 내용 (필요시 저장)
    
    # Relationship
    search_result = relationship("SearchResult", back_populates="articles")

class JobExecutionLog(Base):
    __tablename__ = "job_execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, index=True)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="running") # running, success, failed
    duration = Column(Float, nullable=True)
    message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_processed_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1) # 1: Active, 0: Inactive
