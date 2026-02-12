## Phase 7: 에러 핸들링 강화 및 마무리 (7단계 중 7단계)

---

Phase 7: 에러 핸들링을 강화하고 앱을 마무리합니다.

### 1. 에러 핸들링 강화

#### 환경변수 검증 (config/settings.py)
- 앱 시작 시 필수 환경변수 체크
- 누락 시 명확한 안내 메시지:
  - ".env 파일을 확인해주세요"
  - 각 API 키 발급 방법 안내 링크 제공

```python
# 예시 에러 메시지
"""
❌ 환경변수가 설정되지 않았습니다.

누락된 변수: TAVILY_API_KEY

설정 방법:
1. .env.example 파일을 .env로 복사
2. 각 API 키를 발급받아 입력

API 키 발급 안내:
- Tavily API: https://tavily.com/
- Google AI Studio (Gemini): https://aistudio.google.com/
"""
```

#### API 에러 상세 처리
- Tavily API:
  - 400 (Bad Request) → "잘못된 요청입니다 (API 키 등 확인 필요)"
  - 401 (Unauthorized) → "Tavily API 키가 유효하지 않습니다"
  - 429 (Too Many Requests) → "월간/분당 검색 한도를 초과했습니다"
  - 5xx → "검색 서버 오류, 잠시 후 재시도해주세요"
- Gemini API:
  - 429 → "분당 15회 제한 초과, 30초 후 재시도"
  - 400 → "요청 형식 오류"

#### 네트워크 타임아웃
- requests 타임아웃: 10초
- 타임아웃 발생 시 재시도 1회

---

### 2. UX 개선

#### 진행 상태 표시
- 검색 중: "🔍 뉴스를 검색하고 있습니다..."
- 요약 중: "🤖 AI가 요약하고 있습니다..."
- 저장 중: "💾 결과를 저장하고 있습니다..."

#### 성공 메시지
```python
st.success(f"'{keyword}' 검색 완료! {len(articles)}건의 뉴스를 찾았습니다.")
```

#### 빈 상태 처리
- 첫 실행 시: 환영 메시지 + 사용법 간략 안내
- 검색 기록 없을 때: "아직 검색 기록이 없습니다. 키워드를 입력해 첫 검색을 시작해보세요!"

---

### 3. 코드 정리

#### 린팅 및 포매팅
- 모든 파일 타입 힌트 확인
- docstring 추가 (함수/클래스)
- 불필요한 import 제거

#### README.md 생성
```markdown
# initial_version

키워드로 구글 뉴스를 검색하고 AI가 요약해주는 웹앱

## 설치 방법

### 1. uv 설치 (없는 경우)
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

### 2. 의존성 설치
uv sync

### 3. 환경변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

### 4. 실행
uv run streamlit run app.py

## API 키 발급 안내

### Tavily API (Search)
1. https://tavily.com/ 접속 및 가입
2. API 키 발급 (기본 무료 Plan)
3. `.env` 파일의 `TAVILY_API_KEY`에 입력
4. `SEARCH_DOMAINS`에 검색할 도메인 입력

### Google AI Studio (Gemini)
1. https://aistudio.google.com/ 접속
2. API 키 발급

## 폴더 구조
(폴더 구조 설명)
```

---

### 4. 최종 테스트 체크리스트

- [ ] .env 없이 실행 시 적절한 안내
- [ ] 잘못된 API 키로 실행 시 에러 메시지
- [ ] 정상 검색 → 요약 → 저장 → 조회 전체 흐름
- [ ] CSV 다운로드
- [ ] 검색 결과 없을 때 처리
- [ ] 네트워크 끊겼을 때 처리

---

### 구현 요구사항
- 모든 에러 메시지는 사용자 친화적으로 작성
- 기술적 에러 내용은 로그로만 기록
- README.md는 초보자도 따라할 수 있도록 상세히 작성

---

### 검증 방법

```bash
# .env 없이 실행 테스트
mv .env .env.backup
uv run streamlit run app.py
# 친절한 안내 메시지 확인 후 복원
mv .env.backup .env

# 전체 E2E 테스트
uv run streamlit run app.py
# 1. 키워드 입력 및 검색
# 2. AI 요약 결과 확인
# 3. CSV 저장 확인 (data/search_history.csv)
# 4. 검색 기록 선택하여 조회
# 5. CSV 다운로드
```

---

### 검증 포인트

- [ ] .env 없이 실행 시 친절한 안내 메시지 표시
- [ ] 잘못된 API 키 사용 시 명확한 에러 메시지 표시
- [ ] 전체 E2E 흐름 테스트 통과 (검색 → 요약 → 저장 → 조회 → 다운로드)
- [ ] 검색 결과 없을 때 적절한 안내 메시지 표시
- [ ] 네트워크 오류 시 적절한 에러 메시지 표시
- [ ] README.md 가독성 확인 (설치부터 실행까지 따라할 수 있는지)
- [ ] 모든 함수/클래스에 docstring 추가 확인

---

---

### ⚠️ 필수 요구사항: 한글 사용

**최종 점검 - 모든 UI가 한글인지 확인해주세요:**
- 환경변수 누락 안내 메시지
- API 에러 메시지
- 진행 상태 표시 메시지
- 성공/실패 메시지
- 빈 상태 안내 메시지
- README.md 제외 모든 사용자 대면 텍스트

**앱 실행 시 영어로 된 UI 텍스트가 보이면 한글로 수정해주세요!**

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**