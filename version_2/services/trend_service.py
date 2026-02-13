import logging
import pandas as pd
from services.trend_source import TrendSource

# Set up logging
logger = logging.getLogger(__name__)

class TrendService(TrendSource):
    """
    Service for fetching trending keywords.
    NOTE: Google Trends connection has been removed as per user request (2026-02-13).
    This service now acts as a placeholder and returns empty results for trends.
    Subscription keywords are handled separately in AutomationService.
    """
    def __init__(self, hl='ko-KR', tz=540):
        self.categories = {
            'all': 'all',
            'business': 'b',
            'entertainment': 'e',
            'health': 'm',
            'sci_tech': 't',
            'sports': 's'
        }

    def get_trending_keywords(self, category='all', limit=10):
        """
        Fetches trending keywords.
        Currently disabled/removed connection to Google Trends.
        Returns empty list.
        """
        logger.info("Google Trends connection is disabled. Returning empty list for trending keywords.")
        return []

    def get_available_categories(self):
        return list(self.categories.keys())

    def get_interest_over_time(self, keyword, timeframe='today 1-m'):
        """
        Fetch interest over time for a specific keyword.
        Currently disabled/removed connection to Google Trends.
        Returns empty DataFrame.
        """
        logger.info(f"Google Trends connection is disabled. Returning empty DataFrame for interest over time: {keyword}")
        return pd.DataFrame()
