from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database.session import SessionLocal
from domain.models import JobExecutionLog
import traceback

class MonitoringService:
    """Service to track scheduler status and execution history using database."""
    _instance = None
    
    # In-memory cache to map job_name -> current db_log_id
    # This is to quickly update the correct row on completion
    _active_jobs: Dict[str, int] = {}
    
    # Error threshold for alerting
    ERROR_THRESHOLD = 3
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MonitoringService, cls).__new__(cls)
        return cls._instance

    def log_job_start(self, job_name: str) -> int:
        """Log when a job starts. Returns the log ID."""
        db = SessionLocal()
        try:
            new_log = JobExecutionLog(
                job_name=job_name,
                start_time=datetime.now(),
                status="running"
            )
            db.add(new_log)
            db.commit()
            db.refresh(new_log)
            
            # Update cache
            self._active_jobs[job_name] = new_log.id
            logging.info(f"Job {job_name} started (ID: {new_log.id})")
            return new_log.id
        except Exception as e:
            logging.error(f"Failed to log job start for {job_name}: {e}")
            return -1
        finally:
            db.close()

    def log_job_completion(self, job_name: str, success: bool, message: str = ""):
        """Log when a job completes (success or failure)."""
        db = SessionLocal()
        try:
            log_id = self._active_jobs.get(job_name)
            
            # If we don't have the ID in memory, try to find the last running job
            log_entry = None
            if log_id:
                log_entry = db.query(JobExecutionLog).filter(JobExecutionLog.id == log_id).first()
            
            if not log_entry:
                # Fallback: find most recent running job for this name
                log_entry = (db.query(JobExecutionLog)
                             .filter(JobExecutionLog.job_name == job_name, JobExecutionLog.status == "running")
                             .order_by(desc(JobExecutionLog.start_time))
                             .first())
                
            if not log_entry:
                logging.warning(f"Could not find running job log for {job_name} to complete.")
                # Optional: Create a new 'finished' entry if needed, but for now skip
                return

            end_time = datetime.now()
            duration = (end_time - log_entry.start_time).total_seconds()
            status = "success" if success else "failed"

            log_entry.end_time = end_time
            log_entry.status = status
            log_entry.duration = duration
            log_entry.message = message
            
            if not success:
               log_entry.error_traceback = message # Using message as simple traceback/error msg
            
            db.commit()
            
            # Remove from active cache
            if job_name in self._active_jobs:
                del self._active_jobs[job_name]

            logging.info(f"Job {job_name} completed: {status} in {duration:.2f}s")
            
            # Check for consecutive failures
            if not success:
                self._check_consecutive_failures(db, job_name)

        except Exception as e:
            logging.error(f"Failed to log job completion for {job_name}: {e}")
            traceback.print_exc()
        finally:
            db.close()

    def _check_consecutive_failures(self, db: Session, job_name: str):
        """Check if the job has failed N times in a row and log a warning."""
        recent_logs = (db.query(JobExecutionLog)
                       .filter(JobExecutionLog.job_name == job_name)
                       .order_by(desc(JobExecutionLog.start_time))
                       .limit(self.ERROR_THRESHOLD)
                       .all())
        
        if len(recent_logs) < self.ERROR_THRESHOLD:
            return

        # Check if all recent logs are failures
        if all(log.status == "failed" for log in recent_logs):
            logging.critical(f"ALERT: Job '{job_name}' has failed {self.ERROR_THRESHOLD} consecutive times!")
            # In a real app, you might send an email or Slack notification here.

    def get_scheduler_status(self) -> Dict:
        """Get overall system status and recent stats."""
        db = SessionLocal()
        try:
            # Check for active running jobs
            active_count = db.query(JobExecutionLog).filter(JobExecutionLog.status == "running").count()
            
            # Get last run info
            last_run = (db.query(JobExecutionLog)
                        .order_by(desc(JobExecutionLog.start_time))
                        .first())
            
            total_runs = db.query(JobExecutionLog).count()
            
            failed_runs_24h = (db.query(JobExecutionLog)
                               .filter(JobExecutionLog.status == "failed", 
                                       JobExecutionLog.start_time >= datetime.now() - timedelta(days=1))
                               .count())
            
            return {
                "active_jobs": active_count,
                "last_run_time": last_run.start_time if last_run else None,
                "last_run_status": last_run.status if last_run else "N/A",
                "total_runs": total_runs,
                "failed_runs_24h": failed_runs_24h
            }
        except Exception as e:
            logging.error(f"Error getting scheduler status: {e}")
            return {}
        finally:
            db.close()

    def get_logs(self, limit: int = 10) -> List[Dict]:
        """Get recent job logs."""
        db = SessionLocal()
        try:
            logs = (db.query(JobExecutionLog)
                    .order_by(desc(JobExecutionLog.start_time))
                    .limit(limit)
                    .all())
            
            return [
                {
                    "job_name": log.job_name,
                    "start_time": log.start_time,
                    "end_time": log.end_time,
                    "status": log.status,
                    "duration": log.duration,
                    "message": log.message
                } 
                for log in logs
            ]
        except Exception as e:
            logging.error(f"Error fetching logs: {e}")
            return []
        finally:
            db.close()
