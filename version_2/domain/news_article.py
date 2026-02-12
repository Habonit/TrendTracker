from dataclasses import dataclass

@dataclass
class NewsArticle:
    """
    뉴스 기사 정보의 정보를 담는 데이터 클래스.
    """
    title: str       # 기사 제목
    url: str         # 기사 URL
    snippet: str     # 기사 스니펫 (내용 요약)
    pub_date: str = "" # 발행일 (YYYY-MM-DD 형식 권장)
