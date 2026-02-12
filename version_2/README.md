# TrendTracker (트렌드트래커) 📊

키워드로 최신 뉴스를 검색하고, Google Gemini AI를 통해 핵심 내용을 불릿 포인트로 요약해 주는 실시간 뉴스 트렌드 분석 웹 애플리케이션입니다.

---

## 🌟 주요 기능

- **실시간 뉴스 검색**: Tavily Search API를 사용하여 최신 뉴스 정보를 신속하게 수집합니다.
- **AI 핵심 요약**: Google Gemini API를 활용하여 여러 뉴스의 통찰을 담은 요약문을 생성합니다.
- **검색 기록 관리**: 과거 검색 결과를 CSV 파일에 자동 저장하며, 언제든 다시 조회할 수 있습니다.
- **데이터 내보내기**: 모든 검색 데이터를 CSV 형식으로 다운로드하여 관리할 수 있습니다.

---

## 🛠️ 설치 및 설정 방법

### 1. 전제 조건 (`uv` 사용 권장)

기본적으로 `uv` 패키지 매니저를 사용하여 시스템 설정의 번거로움을 최소화합니다.

#### uv 설치 (없는 경우)
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. 프로젝트 의존성 설치
```bash
uv sync
```

### 3. 환경변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래 API 키들을 입력해야 합니다.

1. `.env.example` 파일을 복사하여 `.env` 생성:
   ```bash
   cp .env.example .env
   ```
2. `.env` 파일을 열고 다음 키값들을 입력:
   - `TAVILY_API_KEY`: [Tavily 홈페이지](https://tavily.com/)에서 발급
   - `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)에서 발급
   - `CSV_PATH`: 데이터 저장 경로 (기본값: `data/search_history.csv`)

---

## 🚀 실행 방법

아래 명령어를 통해 Streamlit 서버를 실행합니다.
```bash
uv run streamlit run app.py
```
실행 후 브라우저에서 `http://localhost:8501`로 접속할 수 있습니다.

---

## 📁 폴더 구성

```text
initial_version/
├── app.py                # 메인 애플리케이션 진입점
├── components/           # UI 컴포넌트 (사이드바, 결과창 등)
├── services/             # 비즈니스 로직 (뉴스 검색, AI 요약)
├── repositories/         # 데이터 영속성 (CSV 관리)
├── domain/               # 데이터 모델 (NewsArticle, SearchResult)
├── config/               # 환경 설정
├── utils/                # 유틸리티 (에러 처리, 키 생성 등)
├── data/                 # 검색 결과 저장 디렉토리 (자동 생성)
└── prompts/              # 개발 단계 안내 문서
```

---

## ⚠️ 주의 사항
- **API 한도**: 무료 플랜 사용 시 Tavily는 월 1,000건, Gemini는 분당 요청 수(RPM) 제한이 있습니다.
- **데이터 영속성**: `data/search_history.csv` 파일을 삭제하면 이전 검색 기록이 유실됩니다. 정기적으로 'CSV 다운로드'를 통해 백업하세요.

---

## 🚫 금지 사항
이 프로젝트는 교육 및 시연 목적으로 작성되었으며, Git/GitHub 관련 작업은 프로젝트 규칙에 따라 수동으로 진행되지 않습니다.
