from google import genai
from typing import List
from domain.news_article import NewsArticle
from config.settings import settings
from utils.exceptions import AppError

def summarize_news(articles: List[NewsArticle]) -> str:
    """
    Gemini API를 사용하여 뉴스 기사들의 핵심 내용을 요약합니다.

    Args:
        articles (List[NewsArticle]): 요약할 기사 리스트

    Returns:
        str: AI가 요약한 한국어 텍스트

    Raises:
        AppError: API 키 오류, 할당량 초과, AI 서비스 오류 등 발생 시
    """
    if not settings or not settings.GEMINI_API_KEY:
        raise AppError("api_key_invalid")
        
    if not articles:
        return "요약할 뉴스 기사가 없습니다."
        
    attempts = 0
    max_retries = 1
    
    while attempts <= max_retries:
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            # 뉴스 목록 텍스트 구성
            news_list_content = ""
            for i, article in enumerate(articles, 1):
                news_list_content += f"{i}. 제목: {article.title}\n   내용: {article.snippet}\n\n"
                
            # 프롬프트 구성 (한국어 요약 요청)
            prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_list_content}
""".strip()
            
            # Gemini 모델 호출
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )
            
            if not response or not response.text:
                raise AppError("ai_error")
                
            return response.text
            
        except Exception as e:
            attempts += 1
            error_msg = str(e).lower()
            
            # 재시도 가능한 에러 (일시적 네트워크 문제)
            is_retryable = "timeout" in error_msg or "connection" in error_msg or "500" in error_msg
            if is_retryable and attempts <= max_retries:
                import time
                time.sleep(1)
                continue
                
            # Gemini Error mapping
            if "api key" in error_msg or "invalid" in error_msg or "401" in error_msg:
                raise AppError("api_key_invalid")
            elif "429" in error_msg or "rate limit" in error_msg or "quota" in error_msg:
                raise AppError("rate_limit_exceeded")
            elif "400" in error_msg:
                raise AppError("bad_request")
            else:
                raise AppError("ai_error")
