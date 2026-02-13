from datetime import datetime, timedelta
from sqlalchemy import desc
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource, NewsArticle
from domain.additional_models import DailyTrendReport
from services.ai_service import summarize_news, generate_daily_insight
from config.settings import settings
import logging

class ReportService:
    """지난 24시간 동안 수집된 트렌드를 종합하여 일간 리포트를 작성합니다."""
    
    def generate_daily_report(self) -> str:
        db = SessionLocal()
        try:
            # 1. 최근 24시간 데이터 가져오기
            yesterday = datetime.now() - timedelta(days=1)
            
            trends = (db.query(SearchResult)
                      .filter(SearchResult.created_at >= yesterday)
                      .order_by(desc(SearchResult.created_at))
                      .limit(10) # 상위 10개만 리포트에 사용
                      .all())
            
            if not trends:
                return "트렌드 데이터가 충분하지 않습니다."

            # 2. 리포트 생성을 위한 트렌드 컨텍스트 구성
            context = ""
            for t in trends:
                # 키워드와 요약 내용을 포함
                summary_snippet = t.ai_summary[:200].replace('\n', ' ') if t.ai_summary else "요약 없음"
                context += f"- 키워드: {t.keyword}\n  요약: {summary_snippet}\n"
                
            # 3. AI에게 리포트 작성 요청 (generate_daily_insight 사용)
            report_content = generate_daily_insight(context)
            
            # 리포트 제목 추가 (AI 응답에 제목이 없을 경우를 대비해 앞단에 붙임)
            # 만약 AI가 잘 생성한다면 중복될 수 있으므로, 단순 저장 혹은 확인 후 저장.
            # 여기서는 AI 응답을 그대로 신뢰하되, 날짜 메타데이터는 DB에 별도 저장됨.

            
            # Save Report to DB
            new_report = DailyTrendReport(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                content=report_content
            )
            db.add(new_report)
            db.commit()
            
            logging.info("Daily report generated successfully.")
            return report_content
            
        except Exception as e:
            logging.error(f"Failed to generate daily report: {e}")
            return None
        finally:
            db.close()

    def get_latest_report(self):
        db = SessionLocal()
        try:
            return (db.query(DailyTrendReport)
                    .order_by(DailyTrendReport.created_at.desc())
                    .first())
        finally:
            db.close()
