from database.session import SessionLocal
from domain.models import Subscription
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

class SubscriptionService:
    """
    Service to manage keyword subscriptions (pinning).
    """
    def get_subscriptions(self):
        """Get all active subscriptions."""
        db = SessionLocal()
        try:
            return db.query(Subscription).filter(Subscription.is_active == 1).all()
        finally:
            db.close()

    def get_all_keywords(self):
        """Get list of active subscription keywords."""
        subs = self.get_subscriptions()
        return [s.keyword for s in subs]

    def add_subscription(self, keyword: str) -> bool:
        """Add a new subscription or reactivate existing one."""
        db = SessionLocal()
        try:
            existing = db.query(Subscription).filter(Subscription.keyword == keyword).first()
            if existing:
                existing.is_active = 1
                db.commit()
                logger.info(f"Reactivated subscription for {keyword}")
                return True
            
            new_sub = Subscription(keyword=keyword)
            db.add(new_sub)
            db.commit()
            logger.info(f"Added subscription for {keyword}")
            return True
        except IntegrityError:
            db.rollback()
            return False
        except Exception as e:
            logger.error(f"Error adding subscription {keyword}: {e}")
            return False
        finally:
            db.close()

    def remove_subscription(self, keyword: str) -> bool:
        """Deactivate a subscription."""
        db = SessionLocal()
        try:
            sub = db.query(Subscription).filter(Subscription.keyword == keyword).first()
            if sub:
                sub.is_active = 0
                db.commit()
                logger.info(f"Removed subscription for {keyword}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing subscription {keyword}: {e}")
            return False
        finally:
            db.close()
