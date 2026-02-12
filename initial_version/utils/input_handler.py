from typing import Optional

def preprocess_keyword(raw_input: str) -> Optional[str]:
    """
    앞뒤 공백 제거 (trim)
    최대 100자 제한
    빈 문자열이면 None 반환
    """
    if not raw_input:
        return None
    
    processed = raw_input.strip()
    if not processed:
        return None
        
    return processed[:100]
