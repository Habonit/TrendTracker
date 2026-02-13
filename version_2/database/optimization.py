
import logging
import sqlite3
import os
from datetime import datetime, timedelta
from sqlalchemy import text
from database.session import SessionLocal, DB_PATH
from domain.models import SearchResult, JobExecutionLog
import pandas as pd

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """
    Service for maintaining database performance and managing data size.
    """
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def optimize(self):
        """
        Run SQLite optimization commands (VACUUM, ANALYZE).
        Should be scheduled to run during low-traffic periods.
        """
        try:
            logger.info("Starting database optimization...")
            
            # Connect directly for administrative commands
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Rebuilds the database file, repacking it into a minimal amount of disk space
                cursor.execute("VACUUM;")
                
                # Gathers statistics about tables and indices and stores them in internal tables
                cursor.execute("ANALYZE;")
                
            logger.info("Database optimization completed successfully.")
            return True
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            return False

    def archive_old_data(self, retention_days: int = 30, export_csv: bool = True):
        """
        Archive or delete data older than retention_days.
        
        Args:
            retention_days (int): Number of days to keep data.
            export_csv (bool): If True, save deleted data to CSV before deletion.
        """
        db = SessionLocal()
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            logger.info(f"Starting archiving for data older than {cutoff_date}...")
            
            # 1. Find old SearchResults
            old_results_query = db.query(SearchResult).filter(SearchResult.created_at < cutoff_date)
            count = old_results_query.count()
            
            if count == 0:
                logger.info("No old data to archive.")
                return 0

            # 2. Export to CSV if requested
            if export_csv:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_dir = os.path.join("data", "archive")
                os.makedirs(archive_dir, exist_ok=True)
                
                df = pd.read_sql(old_results_query.statement, db.bind)
                filename = os.path.join(archive_dir, f"search_results_archive_{timestamp}.csv")
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                logger.info(f"Archived {count} records to {filename}")

            # 3. Delete from DB
            # Use synchronize_session=False for bulk delete performance
            deleted_rows = old_results_query.delete(synchronize_session=False)
            
            # Also clean up old job logs (keep last 7 days usually, but let's use same retention for now)
            db.query(JobExecutionLog).filter(JobExecutionLog.start_time < cutoff_date).delete(synchronize_session=False)
            
            db.commit()
            logger.info(f"Deleted {deleted_rows} old records from database.")
            
            return deleted_rows

        except Exception as e:
            logger.error(f"Data archiving failed: {e}")
            db.rollback()
            return 0
        finally:
            db.close()
