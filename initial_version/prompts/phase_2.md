## Phase 2: 도메인 모델 및 유틸리티 함수 (7단계 중 2단계)

---

Phase 2: 도메인 모델과 유틸리티 함수를 구현합니다.

### 1. 도메인 모델 (domain/)

#### domain/news_article.py
뉴스 기사를 표현하는 NewsArticle 데이터클래스:
- title: str (기사 제목)
- url: str (기사 URL)
- snippet: str (기사 스니펫)

#### domain/search_result.py
검색 결과를 표현하는 SearchResult 데이터클래스:
- search_key: str (PK, "키워드-yyyymmddhhmm" 형식)
- search_time: datetime (검색 실행 시간)
- keyword: str (검색 키워드)
- articles: List[NewsArticle] (뉴스 기사 리스트)
- ai_summary: str (AI 요약 결과)

SearchResult에는 CSV 저장을 위해 Long format(기사 1건=1행)으로 변환하는 `to_dataframe()` 메서드를 추가해주세요.

---

### 2. 유틸리티 함수 (utils/)

#### utils/key_generator.py
- `generate_search_key(keyword: str) -> str`
- 형식: "키워드-yyyymmddhhmm" (예: "AI트렌드-202601181430")
- 현재 시간 기준으로 생성

#### utils/input_handler.py
- `preprocess_keyword(raw_input: str) -> Optional[str]`
- 앞뒤 공백 제거 (trim)
- 최대 100자 제한
- 빈 문자열이면 None 반환

#### utils/error_handler.py
- ERROR_MESSAGES 딕셔너리:
  - api_key_invalid: "API 키를 확인해주세요"
  - daily_limit_exceeded: "일일 검색 한도(100건)를 초과했습니다"
  - rate_limit_exceeded: "잠시 후 다시 시도해주세요 (분당 15회 제한)"
  - no_results: "검색 결과가 없습니다"
  - network_error: "네트워크 연결을 확인해주세요"
  - file_error: "파일 접근에 실패했습니다"
  - empty_input: "검색어를 입력해주세요"
- `handle_error(error_type: str, level: str = "error")` 함수
  - level에 따라 st.error(), st.warning(), st.info() 호출

---

### 구현 요구사항
- Python dataclass를 사용
- 타입 힌트를 명확히 작성
- 각 파일에 적절한 import 추가

---

### 검증 방법

```bash
# 도메인 모델 import 테스트
python -c "from domain.news_article import NewsArticle; print('NewsArticle import 성공')"
python -c "from domain.search_result import SearchResult; print('SearchResult import 성공')"

# 유틸리티 함수 테스트
python -c "from utils.key_generator import generate_search_key; print(generate_search_key('테스트'))"
python -c "from utils.input_handler import preprocess_keyword; print(preprocess_keyword('  테스트  '))"
```

---

### 검증 포인트

- [ ] `from domain.news_article import NewsArticle` import 성공
- [ ] `from domain.search_result import SearchResult` import 성공
- [ ] `generate_search_key("테스트")` 실행 시 "테스트-yyyymmddhhmm" 형식 출력
- [ ] `preprocess_keyword("  테스트  ")` 실행 시 "테스트" 반환
- [ ] `preprocess_keyword("")` 실행 시 None 반환
- [ ] SearchResult의 `to_dataframe()` 메서드가 pandas DataFrame 반환

---

---

### ⚠️ 필수 요구사항: 한글 사용

**모든 UI 텍스트와 사용자에게 보여지는 메시지는 반드시 한글로 작성해주세요:**
- 에러 메시지 (ERROR_MESSAGES 딕셔너리)
- 안내 메시지
- 버튼 텍스트
- 레이블
- 주석 및 docstring은 영어/한글 무관

예시:
- ❌ "No results found"
- ✅ "검색 결과가 없습니다"

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**