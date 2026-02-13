import logging
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import traceback

# Import Monitoring Service
from services.monitoring_service import MonitoringService

logger = logging.getLogger(__name__)

def job_wrapper(job_func, job_name, **kwargs):
    """
    Wrapper to handle logging and error tracking for scheduled jobs.
    """
    monitor = MonitoringService()
    
    # 1. Log Start
    try:
        monitor.log_job_start(job_name)
        
        # 2. Execute Job
        job_func(**kwargs)
        
        # 3. Log Success
        monitor.log_job_completion(job_name, success=True, message="Job completed successfully")
        
    except Exception as e:
        # 4. Log Failure
        error_msg = f"{str(e)}"
        logger.error(f"Job {job_name} failed: {error_msg}")
        traceback.print_exc()
        monitor.log_job_completion(job_name, success=False, message=error_msg)

class SchedulerManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SchedulerManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the scheduler."""
        # Using MemoryJobStore for simplicity. 
        # For persistence across server restarts, SQLAlchemyJobStore would be needed.
        self.scheduler = BackgroundScheduler()
        self.job_id = "trend_automation_job"
        
        # Ensure scheduler stops when app exits (though daemon threads help)
        import atexit
        atexit.register(lambda: self.shutdown())

    def start(self):
        """Start the scheduler if not already running."""
        with self._lock:
            if not self.scheduler.running:
                try:
                    self.scheduler.start()
                    logger.info("Scheduler started successfully.")
                except Exception as e:
                    logger.error(f"Failed to start scheduler: {e}")

    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shutdown.")

    def update_job(self, job_func, interval_minutes: float, **kwargs):
        """
        Add or update the automation job with monitoring wrapper.
        
        Args:
            job_func: The function to execute
            interval_minutes: Execution interval in minutes (can be float < 1 for seconds)
            **kwargs: Arguments to pass to the job function
        """
        try:
            # Remove existing job
            if self.scheduler.get_job(self.job_id):
                self.scheduler.remove_job(self.job_id)
                logger.info(f"Removed existing job: {self.job_id}")

            # Calculate seconds
            seconds = int(interval_minutes * 60)
            if seconds < 10: 
                seconds = 10 # Minimum interval safety
            
            trigger = IntervalTrigger(seconds=seconds)
            
            # Add job with wrapper
            self.scheduler.add_job(
                job_wrapper,
                trigger=trigger,
                id=self.job_id,
                kwargs={
                    "job_func": job_func, 
                    "job_name": "Trend Automation", 
                    **kwargs
                },
                replace_existing=True,
                max_instances=1,
                coalesce=True,
                misfire_grace_time=120,
                next_run_time=datetime.now() # Run immediately on update
            )
            logger.info(f"Updated job {self.job_id} to run every {seconds} seconds.")
            
        except Exception as e:
            logger.error(f"Failed to update job {self.job_id}: {e}")

    def get_job_info(self):
        """Get information about the current automation job."""
        job = self.scheduler.get_job(self.job_id)
        if job:
            return {
                "next_run_time": job.next_run_time,
                "is_running": self.scheduler.running
            }
        return None
