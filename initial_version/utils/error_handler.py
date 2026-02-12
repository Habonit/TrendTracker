import streamlit as st

ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않거나 설정되지 않았습니다. .env 파일을 확인해주세요.",
    "daily_limit_exceeded": "Tavily 월간/일일 검색 한도를 초과했습니다.",
    "rate_limit_exceeded": "분당 요청 제한을 초과했습니다. 잠시 후(약 30초) 다시 시도해주세요.",
    "no_results": "검색 결과가 없습니다.",
    "network_error": "네트워크 서버 오류가 발생했습니다. 잠시 후 재시도해주세요.",
    "file_error": "파일 접근에 실패했습니다.",
    "empty_input": "검색어를 입력해주세요.",
    "ai_error": "AI 요약 중 오류가 발생했습니다. 다시 시도해주세요.",
    "bad_request": "잘못된 요청입니다. 입력값 또는 설정을 확인해주세요."
}

def handle_error(error_type: str, level: str = "error"):
    """
    level에 따라 st.error(), st.warning(), st.info() 호출
    """
    message = ERROR_MESSAGES.get(error_type, "알 수 없는 에러가 발생했습니다")
    
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)
    else:
        st.write(message)
