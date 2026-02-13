from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time
import random
import logging

from services.trend_source import TrendSource

# Set up logging
logger = logging.getLogger(__name__)

class TrendService(TrendSource):
    def __init__(self, hl='ko-KR', tz=540):
        self.pytrends = TrendReq(hl=hl, tz=tz, timeout=(10,25))
        self.categories = {
            'all': 'all',
            'business': 'b',
            'entertainment': 'e',
            'health': 'm',
            'sci_tech': 't',
            'sports': 's'
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ResponseError, ConnectionError))
    )
    def get_trending_keywords(self, category='all', limit=10):
        """
        Fetches trending keywords from Google Trends for South Korea.
        
        Args:
            category (str): Category code ('all', 'business', 'entertainment', 'health', 'sci_tech', 'sports')
            limit (int): Number of keywords to return
            
        Returns:
            list: List of trending keywords
        """
        try:
            # Random sleep to avoid rate limits
            time.sleep(random.uniform(1.0, 3.0))
            
            # Map category name to code if provided
            cat_code = self.categories.get(category.lower(), 'all')
            
            # Get trending searches for South Korea (pn='south_korea')
            # trending_searches returns a DataFrame
            # Note: For real-time trends involving categories, use real_time_trending_searches if standard one doesn't support categories well
            # Standard method: trending_searches(pn='south_korea')
            # Real-time method: real_time_trending_searches(pn='KR', cat=cat_code)
            
            # Use standard trending searches for stability as real_time_trending_searches is missing
            # Note: Category filtering is not supported in standard trending_searches
            if cat_code != 'all':
                logger.warning(f"Category filtering '{category}' is currently not supported due to API limitations. Fetching general trends.")
            
            try:
                df = self.pytrends.trending_searches(pn='south_korea')
            except Exception as trend_err:
                logger.warning(f"trending_searches failed ({trend_err}), trying today_searches...")
                # Fallback: Daily Search Trends
                # today_searches returns a Series usually
                series = self.pytrends.today_searches(pn='KR')
                df = pd.DataFrame(series) # Convert Series to DataFrame for consistent processing below

            if df.empty:
                logger.warning(f"No trending data found for category: {category}")
                return []
            
            # Extract keywords (usually column 0 or 'title')
            keywords = []
            if 'title' in df.columns:
                keywords = df['title'].tolist()
            elif 'query' in df.columns: # sometimes today_searches result
                 keywords = df['query'].tolist()
            else:
                keywords = df.iloc[:, 0].tolist()
                
            return keywords[:limit]

        except Exception as e:
            logger.error(f"Error fetching trends: {str(e)}")
            raise e

    def get_available_categories(self):
        return list(self.categories.keys())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ResponseError, ConnectionError))
    )
    def get_interest_over_time(self, keyword, timeframe='today 1-m'):
        """
        Fetch interest over time for a specific keyword.
        """
        try:
            time.sleep(random.uniform(1.0, 2.0))
            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='KR')
            data = self.pytrends.interest_over_time()
            if data.empty:
                return pd.DataFrame()
            return data.reset_index() # Returns DataFrame with 'date' and keyword column
        except Exception as e:
            logger.error(f"Error fetching interest over time for {keyword}: {e}")
            return pd.DataFrame()
