Phase 5: UI 컴포넌트 (7단계 중 5단계)

---

Phase 5: Streamlit UI 컴포넌트를 구현합니다.

### 1. 검색 폼 (components/search_form.py)

#### `render_search_form() -> Optional[str]`
- `st.text_input`으로 키워드 입력 필드
- `st.button`으로 "검색" 버튼
- 검색 버튼 클릭 시:
  - 빈 입력이면 `st.warning("검색어를 입력해주세요")` 후 None 반환
  - 유효한 입력이면 전처리된 키워드 반환

---

### 2. 사이드바 (components/sidebar.py)

#### `render_sidebar_header()`
- 제목: "initial_version"
- 소개문: "키워드로 뉴스를 검색하고 AI가 요약해드립니다"

#### `render_settings() -> int`
- "⚙️ 설정" 섹션
- `st.slider`로 검색 건수 설정 (범위 1~10, 기본값 5)
- 선택된 값 반환

#### `render_info()`
- "ℹ️ 사용법" 섹션 (expander)
- 간단한 사용 단계 설명
- "📊 API 한도" 섹션
- "Tavily 무료 플랜: 월 1,000건 검색 가능" 안내
- "💾 데이터 저장 안내" 섹션 (expander)
  - "검색 기록은 CSV 파일(data/search_history.csv)에 저장됩니다."
  - "CSV 파일을 삭제하거나 경로를 변경하면 이전 검색 기록이 모두 사라집니다."
  - "중요한 기록은 CSV 다운로드 기능을 통해 백업해주세요."

#### `render_history_list(search_keys: List[str], keywords_map: dict) -> Optional[str]`
- "📜 검색 기록" 섹션
- `st.selectbox`로 과거 검색 목록
- 표시 형식: "키워드 (yyyy-mm-dd HH:MM)"
- 목록 없으면 "저장된 검색 기록이 없습니다" 표시
- 선택된 search_key 반환

#### `render_download_button(csv_data: str, is_empty: bool)`
- "📥 CSV 다운로드" 버튼
- 파일명: "trendtracker_export_yyyymmdd.csv"
- 데이터 없으면 버튼 비활성화 + 안내 메시지

---

### 3. 결과 화면 (components/result_section.py)

#### `render_summary(title: str, summary: str)`
- `st.subheader`로 제목 표시
- `st.info()` 또는 `st.container()`로 요약 내용 표시

#### `render_news_list(articles: List[NewsArticle])`
- 각 기사를 `st.expander`로 표시
- expander 제목: 기사 제목 + (발행일)
- 내부: 
  - 날짜 정보가 있는 경우 "📅 발행일: YYYY-MM-DD" 표시
  - 스니펫 + URL 링크 ("🔗 기사 보기")

---

### 4. 로딩 상태 (components/loading.py)

#### `show_loading(message: str)`
- `st.spinner`로 로딩 상태 표시
- context manager로 사용 가능하도록 구현

```python
# 사용 예시
with show_loading("뉴스를 검색하고 있습니다..."):
    articles = search_news(keyword)
```

---

### 구현 요구사항
- 모든 컴포넌트는 `st.session_state`를 적절히 활용
- 타입 힌트 명확히 작성
- 각 컴포넌트는 독립적으로 동작 가능하도록 구현

---

### 검증 방법

```bash
# 컴포넌트 import 테스트
python -c "from components.search_form import render_search_form; print('search_form import 성공')"
python -c "from components.sidebar import render_sidebar_header, render_settings; print('sidebar import 성공')"
python -c "from components.result_section import render_summary, render_news_list; print('result_section import 성공')"
python -c "from components.loading import show_loading; print('loading import 성공')"

# Streamlit 앱으로 개별 테스트 (선택)
# 임시 test_components.py 생성 후 streamlit run test_components.py
```

---

### 검증 포인트

- [ ] `from components.search_form import render_search_form` import 성공
- [ ] `from components.sidebar import render_sidebar_header, render_settings, render_info, render_history_list, render_download_button` import 성공
- [ ] `from components.result_section import render_summary, render_news_list` import 성공
- [ ] `from components.loading import show_loading` import 성공
- [ ] 각 컴포넌트 독립 렌더링 테스트 성공
- [ ] 사이드바 slider 값 변경 확인 (1~10 범위)
- [ ] 검색 기록 selectbox 동작 확인

---

---

### ⚠️ 필수 요구사항: 한글 사용

**모든 UI 컴포넌트의 텍스트는 반드시 한글로 작성해주세요:**
- 버튼 텍스트: "검색", "다운로드" 등
- 레이블: "검색어 입력", "검색 건수" 등
- 안내 메시지: "검색어를 입력해주세요", "저장된 검색 기록이 없습니다" 등
- 섹션 제목: "설정", "사용법", "검색 기록" 등
- placeholder 텍스트

예시:
- ❌ "Search", "Enter keyword", "No results"
- ✅ "검색", "키워드를 입력하세요", "검색 결과가 없습니다"

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**