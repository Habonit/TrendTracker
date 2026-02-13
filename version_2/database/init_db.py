from database.session import engine, Base
from domain.models import SearchResult, NewsArticle, JobExecutionLog, Subscription
from domain.additional_models import TrendReliability, DailyTrendReport

def init_db():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
