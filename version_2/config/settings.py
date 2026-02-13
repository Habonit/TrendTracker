import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    """
    애플리케이션 설정을 관리하는 클래스
    """
    def __init__(self):
        # 필수 환경 변수 체크
        self.TAVILY_API_KEY = self._get_required_env("TAVILY_API_KEY", "Tavily API 키가 필요합니다. https://tavily.com/ 에서 발급받으세요.")
        self.GEMINI_API_KEY = self._get_required_env("GEMINI_API_KEY", "Google Gemini API 키가 필요합니다. https://aistudio.google.com/ 에서 발급받으세요.")
        self.CSV_PATH = self._get_required_env("CSV_PATH", "데이터 저장을 위한 CSV 경로(CSV_PATH)가 설정되지 않았습니다.")
        
        # 선택 환경 변수 (기본값 제공)
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # 검색 도메인 설정 (쉼표로 구분된 문자열을 리스트로 변환)
        domains_str = os.getenv("SEARCH_DOMAINS", "")
        if domains_str:
            self.SEARCH_DOMAINS = [d.strip() for d in domains_str.split(",") if d.strip()]
        else:
            self.SEARCH_DOMAINS = []

        # 알림 설정 (Optional)
        self.DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
        self.SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        
        self.EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
        self.EMAIL_SENDER = os.getenv("EMAIL_SENDER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        
        email_recipients_str = os.getenv("EMAIL_RECIPIENTS", "")
        self.EMAIL_RECIPIENTS = [e.strip() for e in email_recipients_str.split(",") if e.strip()]

    def _get_required_env(self, key: str, error_msg: str) -> str:
        """
        필수 환경변수를 가져오고 없으면 에러를 발생시킵니다.
        """
        value = os.getenv(key)
        if not value:
            missing_guide = f"""
❌ 환경변수가 설정되지 않았습니다.

누락된 변수: {key}

설정 방법:
1. .env.example 파일을 .env로 복사 (이미 있다면 내용을 확인)
2. 각 API 키를 발급받아 .env 파일에 입력 후 저장

API 키 발급 안내:
- Tavily API: https://tavily.com/
- Google AI Studio (Gemini): https://aistudio.google.com/
"""
            raise ValueError(missing_guide)
        return value

# 싱글톤 인스턴스 생성
try:
    settings = Settings()
    settings_error = None
except ValueError as e:
    settings_error = str(e)
    settings = None
except Exception as e:
    settings_error = f"설정 로드 중 예기치 못한 오류 발생: {str(e)}"
    settings = None
