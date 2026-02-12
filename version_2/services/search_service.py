from tavily import TavilyClient
from typing import List
from domain.news_article import NewsArticle
from config.settings import settings
from utils.exceptions import AppError

def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    """
    Tavily API를 사용하여 뉴스 기사를 검색합니다.

    Args:
        keyword (str): 검색 키워드
        num_results (int): 가져올 결과 개수 (1~10)

    Returns:
        List[NewsArticle]: 검색된 기사 리스트

    Raises:
        AppError: API 키 오류, 할당량 초과, 네트워크 오류 등 발생 시
    """
    if not settings or not settings.TAVILY_API_KEY:
        raise AppError("api_key_invalid")
        
    attempts = 0
    max_retries = 1
    
    while attempts <= max_retries:
        try:
            client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            
            # 검색 파라미터 설정
            max_search_results = max(num_results * 3, 20)
            include_domains = settings.SEARCH_DOMAINS if settings.SEARCH_DOMAINS else None
            
            # Tavily 검색 호출
            response = client.search(
                query=keyword,
                search_depth="advanced",
                include_domains=include_domains,
                max_results=max_search_results,
                topic="news"
            )
            
            results = response.get('results', [])
            if not results:
                return []
                
            # 최신순 정렬 (날짜 없는 기사는 뒤로)
            sorted_results = sorted(
                results, 
                key=lambda x: x.get('published_date') if x.get('published_date') else "0000-00-00", 
                reverse=True
            )
            
            articles = []
            for res in sorted_results[:num_results]:
                articles.append(NewsArticle(
                    title=res.get('title', '제목 없음'),
                    url=res.get('url', ''),
                    snippet=res.get('content', ''),
                    pub_date=res.get('published_date', '')
                ))
                
            return articles
            
        except Exception as e:
            attempts += 1
            error_msg = str(e).lower()
            
            # 재시도 가능한 에러 (타임아웃, 네트워크 일시 오류) 및 재시도 횟수 확인
            is_retryable = "timeout" in error_msg or "connection" in error_msg or "500" in error_msg
            if is_retryable and attempts <= max_retries:
                import time
                time.sleep(1) # 잠시 대기 후 재시도
                continue
                
            # 에러 매핑 및 발생
            if "401" in error_msg or "unauthorized" in error_msg:
                raise AppError("api_key_invalid")
            elif "429" in error_msg or "rate limit" in error_msg:
                raise AppError("daily_limit_exceeded")
            elif "400" in error_msg:
                raise AppError("bad_request")
            else:
                raise AppError("network_error")
