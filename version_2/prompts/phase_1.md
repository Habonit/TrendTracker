## Phase 1: 프로젝트 초기화 및 환경 설정 (7단계 중 1단계)

---

initial_version 프로젝트를 시작합니다.

### 프로젝트 개요

- 키워드로 구글 뉴스를 검색하고 AI(Gemini)로 핵심 내용을 요약하는 Streamlit 웹앱
- 로컬 환경에서 실행, 데이터는 CSV로 저장

---

### 1단계: uv 설치 확인 및 프로젝트 초기화

```bash
# uv 설치 확인 (없으면 설치)
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 폴더 생성 및 초기화
uv init initial_version
cd initial_version

# Python 3.11 기반 가상환경 생성
uv venv --python 3.11

# 가상환경 활성화
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

```

---

### 2단계: 의존성 패키지 추가

```bash
uv add streamlit pandas google-genai requests python-dotenv tavily-python

```

---

### 3단계: 폴더 구조 생성

다음 폴더 구조로 프로젝트를 생성해주세요:

```
initial_version/
├── .venv/                      # Python 가상환경 (uv venv로 생성됨)
├── pyproject.toml              # 프로젝트 설정 및 의존성 (uv init으로 생성됨)
├── uv.lock                     # 의존성 잠금 파일 (uv add로 생성됨)
├── app.py                      # 메인 Streamlit 앱
├── .env.example                # 환경변수 템플릿
├── config/
│   ├── __init__.py
│   └── settings.py             # 환경 설정 로더
├── domain/
│   └── __init__.py             # 엔티티/데이터 모델
├── repositories/
│   └── __init__.py             # 데이터 접근 계층
├── services/
│   └── __init__.py             # 비즈니스 로직
├── components/
│   └── __init__.py             # UI 컴포넌트
├── utils/
│   └── __init__.py             # 공통 유틸리티
└── data/                       # CSV 저장 폴더

```

---

### 환경 요구사항

- Python 3.11+
- uv (패키지 관리자)
- Streamlit 1.24+
- pandas, google-genai, requests, python-dotenv

---

### 생성할 파일

### 1. .env.example

```
# Tavily API (Search)
TAVILY_API_KEY=tvly-xxxxxxxxxxxx

# Search Configuration
# 검색할 도메인들을 쉼표(,)로 구분하여 입력
SEARCH_DOMAINS=www.hani.co.kr,www.joongang.co.kr,www.khan.co.kr,www.donga.com,www.ytn.co.kr,news.jtbc.co.kr,imnews.imbc.com,www.yna.co.kr,news.kbs.co.kr,news.sbs.co.kr

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

# Data Storage
CSV_PATH=data/search_history.csv

```

### 2. config/settings.py

- dotenv로 환경변수 로드하는 Settings 클래스
- 환경변수 누락 시 명확한 에러 메시지 출력
- 필수 변수: TAVILY_API_KEY, GEMINI_API_KEY, CSV_PATH
- GEMINI_MODEL은 선택 (기본값: "gemini-2.5-flash")
- SEARCH_DOMAINS는 선택(또는 기본값 지정 가능)이나, 가급적 설정을 권장

### 3. 각 폴더에 빈 `__init__.py` 파일

---

### 검증 방법

```bash
# 가상환경 활성화 확인
which python  # .venv/bin/python 경로 출력되어야 함

# 패키지 설치 확인
uv pip list

# settings.py import 테스트
python -c "from config.settings import Settings; print('Settings import 성공')"

```

---

settings.py에서는 환경변수 누락 시 어떤 변수가 누락되었는지, 어떻게 설정해야 하는지 친절한 에러 메시지를 출력하도록 해주세요.

---

### 검증 포인트

- [ ]  `.venv` 가상환경 폴더 생성 확인
- [ ]  가상환경 활성화 확인 (`which python` 실행 시 `.venv` 경로 출력)
- [ ]  `pyproject.toml` 및 `uv.lock` 파일 생성 확인
- [ ]  모든 폴더 구조 생성 확인 (config, domain, repositories, services, components, utils, data)
- [ ]  `uv pip list`로 패키지 설치 확인
- [ ]  `from config.settings import Settings` import 성공

---

### 중요 안내 (Phase 1 완료 후 반드시 출력할 것)

Phase 1이 완료되면 다음 안내문구를 반드시 마지막에 출력해주세요:

```
⚠️ 중요: 다음 단계로 넘어가기 전에 .env 파일을 반드시 설정해주세요!

1. .env.example 파일을 .env로 복사합니다:
   cp .env.example .env

2. .env 파일을 열어 다음 API 키를 모두 입력해주세요:
   - TAVILY_API_KEY: Tavily 웹사이트에서 발급
   - SEARCH_DOMAINS: 검색하고 싶은 뉴스/테크 사이트 도메인 (쉼표로 구분)
   - GEMINI_API_KEY: Google AI Studio에서 발급

API 키 발급 안내:
- Tavily API: https://tavily.com/
- Google AI Studio (Gemini): https://aistudio.google.com/

모든 API 키가 설정되어야 앱이 정상 동작합니다!
```

---

모든 UI와 중간 과정은 모두 한글로 작성해주세요.

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**