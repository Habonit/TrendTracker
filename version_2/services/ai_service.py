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


def generate_daily_insight(trend_context: str) -> str:
    """
    일간 트렌드 리포트를 위한 인사이트를 생성합니다.
    """
    if not settings.GEMINI_API_KEY:
        return "API 키가 설정되지 않아 리포트를 생성할 수 없습니다."
        
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""
당신은 트렌드 분석 전문가입니다. 다음은 지난 24시간 동안 수집된 주요 뉴스 트렌드 목록입니다.
이를 바탕으로 '일간 트렌드 인사이트 리포트'를 작성해주세요.

[구성 요소]
1. 🌟 **오늘의 핵심 키워드**: 가장 중요한 키워드 3개를 선정하고 이유를 한 줄로 설명하세요.
2. 📈 **시장/사회 영향 분석**: 위 트렌드들이 경제, 기술, 또는 사회에 미칠 잠재적 영향을 2~3문장으로 분석하세요.
3. 📝 **종합 요약**: 전체적인 흐름을 3줄 내외로 요약하세요.

[트렌드 데이터]
{trend_context}

작성 언어: 한국어
톤앤매너: 전문적이고 통찰력 있게
""".strip()

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )
        
        return response.text if response and response.text else "리포트 생성에 실패했습니다."
        
    except Exception as e:
        return f"AI 서비스 오류로 리포트를 생성할 수 없습니다: {str(e)}"
