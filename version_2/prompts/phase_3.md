## Phase 3: 서비스 레이어 - API 연동 (7단계 중 3단계)

---

Phase 3: 외부 API 연동 서비스를 구현합니다.

### 1. 뉴스 검색 서비스 (services/search_service.py)

#### Tavily API 연동
- 라이브러리: `tavily-python` (TavilyClient)
- 홈페이지: https://tavily.com

#### `search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]`
- 환경변수 `TAVILY_API_KEY`로 `TavilyClient` 초기화
- `tavily.search()` 호출 파라미터:
  - query: 검색 키워드
  - search_depth: "advanced" (검색 품질과 날짜 정확도를 높이기 위해 고급 검색 사용)
  - include_domains: `settings.SEARCH_DOMAINS` (쉼표로 구분된 문자열을 리스트로 변환하여 사용)
  - max_results: `max(num_results * 3, 20)` (충분한 기사를 확보한 뒤 최신순으로 필터링하기 위해 더 많이 가져옴)
  - topic: "news" (뉴스 모드 활성화 - 중요!)
- 결과 처리:
  - 응답(`response['results']`)을 `published_date` 기준 **내림차순(최신순)**으로 정렬
  - 날짜 정보가 없는 기사는 리스트의 하단으로 배치
  - 정렬된 리스트에서 상위 `num_results` 개수만큼만 추출
- 응답의 각 항목에서:
  - title: 기사 제목
  - url: 기사 링크
  - content: 기사 내용/스니펫 → `NewsArticle`의 `snippet` 필드에 매핑
  - published_date: 발행일 → `NewsArticle`의 `pub_date` 필드에 매핑
- NewsArticle 리스트로 반환

#### 예외 처리
- API 키 오류/권한: `AppError("api_key_invalid")` raise
- Rate Limit (429): `AppError("rate_limit_exceeded")` raise
- 검색 결과 없음: 빈 리스트 반환
- 네트워크 오류: `AppError("network_error")` raise

---

### 2. AI 요약 서비스 (services/ai_service.py)

#### Gemini API 연동
- 라이브러리: google-genai
- 모델: `settings.GEMINI_MODEL` (기본값: gemini-2.5-flash)

#### `summarize_news(articles: List[NewsArticle]) -> str`
- 프롬프트 템플릿:
```
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
1. 제목: {title}
   내용: {snippet}
...
```
- 뉴스 스니펫을 하나의 컨텍스트로 구성하여 API 호출

#### 예외 처리
- API 키 오류: `AppError("api_key_invalid")` raise
- Rate Limit (429): `AppError("rate_limit_exceeded")` raise
- 기타 오류: `AppError("ai_error")` raise

---

### 3. 커스텀 예외 클래스 (utils/exceptions.py)

```python
class AppError(Exception):
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)
```

---

### 구현 요구사항
- 각 서비스는 `config.settings`에서 API 키를 가져오도록 구현
- TavilyClient는 `services/search_service.py` 내부에서 초기화 (또는 싱글톤)
- 타입 힌트 명확히 작성

---

### 검증 방법

```bash
# 예외 클래스 import 테스트
python -c "from utils.exceptions import AppError; print('AppError import 성공')"

# 서비스 import 테스트
python -c "from services.search_service import search_news; print('search_service import 성공')"
python -c "from services.ai_service import summarize_news; print('ai_service import 성공')"

# API 키 없이 실행 시 에러 확인 (선택)
python -c "from services.search_service import search_news; search_news('테스트')"
```

---

### 검증 포인트

- [ ] `from utils.exceptions import AppError` import 성공
- [ ] `from services.search_service import search_news` import 성공
- [ ] `from services.ai_service import summarize_news` import 성공
- [ ] API 키 없이 실행 시 적절한 `AppError` 발생
- [ ] 실제 API 호출 테스트 성공 (API 키 설정 후)
- [ ] 빈 결과 처리 확인 (빈 리스트 반환)

---

---

### ⚠️ 필수 요구사항: 한글 사용

**모든 UI 텍스트와 사용자에게 보여지는 메시지는 반드시 한글로 작성해주세요:**
- 에러 메시지
- 안내 메시지
- 프롬프트 템플릿 (한국어로 요약 요청)
- 버튼 텍스트
- 레이블

예시:
- ❌ "API key is invalid"
- ✅ "API 키가 유효하지 않습니다"

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**