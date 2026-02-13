from datetime import datetime

def generate_search_key(keyword: str) -> str:
    """
    형식: "키워드-yyyymmddhhmmss" (예: "AI트렌드-20260118143000")
    현재 시간 기준으로 생성
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{keyword}-{now}"
