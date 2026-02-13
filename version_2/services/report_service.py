from datetime import datetime, timedelta
from sqlalchemy import desc
from database.session import SessionLocal
from domain.models import SearchResult, SearchSource, NewsArticle
from domain.additional_models import DailyTrendReport
from services.ai_service import summarize_news, generate_daily_insight
from config.settings import settings
from utils.pdf_generator import create_wordcloud_image, create_report_html, generate_pdf_from_html
import logging

class ReportService:
    """지난 24시간 동안 수집된 트렌드를 종합하여 일간 리포트를 작성합니다."""
    
    def generate_daily_report(self) -> str:
        db = SessionLocal()
        try:
            yesterday = datetime.now() - timedelta(days=1)
            trends = (db.query(SearchResult)
                      .filter(SearchResult.created_at >= yesterday)
                      .order_by(desc(SearchResult.created_at))
                      .limit(10)
                      .all())
            
            if not trends:
                return "트렌드 데이터가 충분하지 않습니다."

            return self._create_report_from_trends(db, trends, "일간 트렌드 리포트")
            
        except Exception as e:
            logging.error(f"Failed to generate daily report: {e}")
            return None
        finally:
            db.close()

    def generate_custom_report(self, search_keys: list) -> str:
        """선택된 키워드들에 대한 맞춤형 리포트를 생성합니다."""
        db = SessionLocal()
        try:
            trends = (db.query(SearchResult)
                      .filter(SearchResult.search_key.in_(search_keys))
                      .all())
            
            if not trends:
                return "선택된 데이터가 없습니다."
                
            return self._create_report_from_trends(db, trends, "맞춤형 트렌드 리포트")
        except Exception as e:
            logging.error(f"Failed to generate custom report: {e}")
            return None
        finally:
            db.close()

    def generate_custom_pdf_report(self, search_keys: list) -> bytes:
        """선택된 키워드들에 대한 맞춤형 PDF 리포트를 생성합니다."""
        db = SessionLocal()
        try:
            trends = (db.query(SearchResult)
                      .filter(SearchResult.search_key.in_(search_keys))
                      .all())
            
            if not trends:
                return None
            
            # 1. Provide Context for AI Summary
            context = ""
            keywords_freq = {}
            items_for_html = []
            
            for t in trends:
                summary_snippet = t.ai_summary[:200].replace('\n', ' ') if t.ai_summary else "요약 없음"
                context += f"- 키워드: {t.keyword}\n  요약: {summary_snippet}\n"
                
                # Update Freq for WordCloud
                keywords_freq[t.keyword] = keywords_freq.get(t.keyword, 0) + 1
                
                items_for_html.append({
                    "keyword": t.keyword,
                    "source": t.source,
                    "date": t.created_at.strftime("%Y-%m-%d %H:%M"),
                    "summary": t.ai_summary or "내용 없음"
                })

            # 2. AI Summary Generation
            report_summary = generate_daily_insight(context)
            
            # 3. Viz Generation
            # If all freqs are 1, wordcloud might be boring, but still generaing it.
            viz_image = create_wordcloud_image(keywords_freq)
            
            # 4. HTML Generation
            html_content = create_report_html(
                title="TrendTracker Custom Report",
                summary=report_summary,
                viz_image=viz_image, 
                items=items_for_html
            )
            
            # 5. PDF Conversion
            pdf_bytes = generate_pdf_from_html(html_content)
            
            return pdf_bytes
            
        except Exception as e:
            logging.error(f"Failed to generate custom PDF report: {e}")
            return None
        finally:
            db.close()

    def _create_report_from_trends(self, db, trends, report_title="트렌드 리포트"):
        context = ""
        for t in trends:
            summary_snippet = t.ai_summary[:200].replace('\n', ' ') if t.ai_summary else "요약 없음"
            context += f"- 키워드: {t.keyword}\n  요약: {summary_snippet}\n"
            
        report_content = generate_daily_insight(context)
        
        new_report = DailyTrendReport(
            report_date=datetime.now().strftime("%Y-%m-%d"),
            content=f"# {report_title}\n\n{report_content}"
        )
        db.add(new_report)
        db.commit()
        
        logging.info(f"{report_title} generated successfully.")
        return report_content

    def get_latest_report(self):
        db = SessionLocal()
        try:
            return (db.query(DailyTrendReport)
                    .order_by(DailyTrendReport.created_at.desc())
                    .first())
        finally:
            db.close()
