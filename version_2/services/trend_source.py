from abc import ABC, abstractmethod

class TrendSource(ABC):
    @abstractmethod
    def get_trending_keywords(self, category='all', limit=10):
        pass

    @abstractmethod
    def get_available_categories(self):
        pass
