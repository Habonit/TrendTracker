from sqlalchemy import Column, Integer, String, DateTime, Float
from database.session import Base
from datetime import datetime

class TrendReliability(Base):
    __tablename__ = "trend_reliabilities"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # 각 소스별 언급 빈도 또는 점수
    google_score = Column(Float, default=0.0)
    naver_score = Column(Float, default=0.0)
    news_score = Column(Float, default=0.0)
    
    total_score = Column(Float, default=0.0) # 종합 신뢰도 점수 (0~100)
    
class DailyTrendReport(Base):
    __tablename__ = "daily_trend_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(String, index=True, nullable=False) # YYYY-MM-DD
    content = Column(String, nullable=False) # AI generated report content
    created_at = Column(DateTime, default=datetime.now)
