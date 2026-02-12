## Phase 6: 메인 앱 통합 (7단계 중 6단계)

---

Phase 6: app.py에서 모든 컴포넌트를 통합합니다.

### app.py 구현

#### 페이지 설정
```python
st.set_page_config(page_title="initial_version", layout="wide")
```

#### 초기화
- SearchRepository 인스턴스 생성
- `st.session_state` 초기화:
  - current_mode: "new_search" | "history"
  - selected_key: Optional[str]
  - last_result: Optional[SearchResult]

---

### 사이드바 렌더링

1. `render_sidebar_header()`
2. `num_results = render_settings()`
3. `render_info()`
4. 구분선
5. `search_keys = repository.get_all_keys()`
6. keywords_map 생성 (search_key → keyword 매핑)
7. `selected_key = render_history_list(search_keys, keywords_map)`
8. `csv_data = repository.get_all_as_csv()`
9. `render_download_button(csv_data, len(search_keys) == 0)`

---

### 메인 영역 렌더링

#### 새 검색 모드
1. `keyword = render_search_form()`
2. 검색 버튼 클릭 시:
   - `with show_loading("🔍 뉴스를 검색하고 있습니다..."):`
     - `articles = search_news(keyword, num_results)`
   - 결과 없으면 `st.info("검색 결과가 없습니다")`
   - `with show_loading("🤖 AI가 요약하고 있습니다..."):`
     - `summary = summarize_news(articles)`
   - SearchResult 생성 및 저장
   - `render_summary(f"'{keyword}' 키워드 요약", summary)`
   - `render_news_list(articles)`

#### 기록 조회 모드
1. selected_key가 있으면:
   - `result = repository.find_by_key(selected_key)`
   - `render_summary(f"검색 기록: {selected_key}", result.ai_summary)`
   - `render_news_list(result.articles)`

---

### 에러 처리
- 모든 API 호출은 try-except로 감싸기
- AppError 발생 시 `handle_error()` 호출
- 앱 크래시 방지

```python
try:
    articles = search_news(keyword, num_results)
except AppError as e:
    handle_error(e.error_type)
    return
```

---

### 모드 전환 로직
- 검색 폼 제출 시: `current_mode = "new_search"`
- 검색 기록 선택 시: `current_mode = "history"`
- `st.rerun()` 적절히 사용

---

### 흐름 요약

```
[앱 시작] → [사이드바 렌더링] → [메인 영역 렌더링]
                                    ↓
                        [새 검색] or [기록 조회]
                                    ↓
                        [결과 표시 + CSV 저장]
```

---

### 구현 요구사항
- 모든 import 상단에 정리
- `st.session_state` 활용하여 상태 관리
- 에러 발생 시에도 앱 크래시 없이 동작

---

### 검증 방법

```bash
# Streamlit 앱 실행
streamlit run app.py

# 또는 uv로 실행
uv run streamlit run app.py
```

---

### 검증 포인트

- [ ] `streamlit run app.py` 또는 `uv run streamlit run app.py` 정상 실행
- [ ] 사이드바에 설정, 사용법, 검색 기록, 다운로드 버튼 표시
- [ ] 키워드 입력 → 검색 버튼 클릭 → 로딩 표시 → 결과 표시 흐름 완료
- [ ] 검색 완료 후 CSV 파일에 데이터 저장 확인
- [ ] 검색 기록 클릭 → 해당 기록 표시
- [ ] CSV 다운로드 버튼 동작 확인
- [ ] API 에러 발생 시 적절한 에러 메시지 표시 (앱 크래시 없음)

---


---

### ⚠️ 필수 요구사항: 한글 사용

**앱의 모든 UI 텍스트와 메시지는 반드시 한글로 작성해주세요:**
- 로딩 메시지: "뉴스를 검색하고 있습니다...", "AI가 요약하고 있습니다..."
- 성공/에러 메시지
- 안내 문구
- 모든 버튼, 레이블, 제목

**영어로 된 UI 텍스트가 있으면 안 됩니다!**

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**