# TrendTracker 학습 가이드

이 문서는 프로젝트를 7단계 프롬프트 순서에 따라 이해하기 위한 학습 가이드입니다.
각 Phase별로 **프롬프트 역할**, **핵심 개념**, **주요 코드**, **데이터 흐름**을 설명합니다.

---

# 목차

1. [Phase 1: 프로젝트 초기화 및 환경 설정](#phase-1-프로젝트-초기화-및-환경-설정)
2. [Phase 2: 도메인 모델 및 유틸리티 함수](#phase-2-도메인-모델-및-유틸리티-함수)
3. [Phase 3: 서비스 레이어 - API 연동](#phase-3-서비스-레이어---api-연동)
4. [Phase 4: 리포지토리 레이어 - 데이터 관리](#phase-4-리포지토리-레이어---데이터-관리)
5. [Phase 5: UI 컴포넌트](#phase-5-ui-컴포넌트)
6. [Phase 6: 메인 앱 통합](#phase-6-메인-앱-통합)
7. [Phase 7: 에러 핸들링 강화 및 마무리](#phase-7-에러-핸들링-강화-및-마무리)
8. [전체 데이터 흐름 다이어그램](#전체-데이터-흐름-다이어그램)

---

# Phase 1: 프로젝트 초기화 및 환경 설정

## 이 프롬프트의 역할
- 프로젝트의 기반이 되는 폴더 구조를 생성하고, 필요한 패키지를 설치하며 환경변수 관리 체계를 구축합니다.
- 생성된 파일: `pyproject.toml`, `.env.example`, `config/settings.py`

## 학습 목표
- `uv` 패키지 관리자를 이용한 프로젝트 초기화 방법 이해
- 환경변수(`.env`)를 사용하여 API 키 등 민감 정보를 관리하는 이유 학습
- 싱글톤 패턴을 활용한 설정(Settings) 관리 기법 이해

## 이해를 위한 핵심 개념

### 1.1 패키지 매니저 (uv)
`uv`는 Rust로 작성된 매우 빠른 Python 패키지 관리자입니다. `pip`보다 속도가 빠르며 `pyproject.toml`을 통해 프로젝트 의존성을 명확하게 관리합니다.

### 1.2 환경변수 관리 (python-dotenv)
API 키와 같이 코드에 직접 노출되면 안 되는 정보를 별도의 `.env` 파일에 저장하고, 실행 시점에 로드하여 보안을 강화합니다.

## 주요 코드 인용

### config/settings.py - 환경 설정 로더
```python
# config/settings.py:7-15
class Settings:
    """
    애플리케이션 설정을 관리하는 클래스
    """
    def __init__(self):
        # 필수 환경 변수 체크
        self.TAVILY_API_KEY = self._get_required_env("TAVILY_API_KEY", "Tavily API 키가 필요합니다...")
        self.GEMINI_API_KEY = self._get_required_env("GEMINI_API_KEY", "Google Gemini API 키가 필요합니다...")
        self.CSV_PATH = self._get_required_env("CSV_PATH", "데이터 저장을 위한 CSV 경로가 설정되지 않았습니다.")
```

**코드 설명:**
- `Settings` 클래스: 앱 전역에서 사용할 설정값을 한곳에서 관리합니다.
- `_get_required_env`: 필수값이 없을 경우 사용자에게 친절한 가이드를 제공하며 예외를 발생시킵니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 1 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [.env] → [settings.py] → [전역 설정] │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 2: 도메인 모델 및 유틸리티 함수

## 이 프롬프트의 역할
- 앱에서 다룰 데이터의 구조를 정의(Data Class)하고, 공통적으로 사용될 도구 함수들을 구현합니다.
- 생성된 파일: `domain/news_article.py`, `domain/search_result.py`, `utils/key_generator.py` 등

## 학습 목표
- `dataclass`를 사용하여 구조화된 데이터를 정의하는 방법 실습
- 입력 데이터 전처리 및 에러 메시지 중앙 관리 기법 습득
- PK(Primary Key) 생성을 위한 유틸리티 함수 구현 방식 이해

## 이해를 위한 핵심 개념

### 2.1 도메인 모델 (Data Class)
비즈니스 로직에서 사용하는 핵심 데이터를 클래스 형태로 정의한 것입니다. `@dataclass`를 쓰면 `__init__` 등을 자동으로 생성해주어 코드가 간결해집니다.

### 2.2 입력 핸들러 (Input Preprocessing)
사용자가 입력한 검색어의 공백을 제거하거나 길이를 제한함으로써 시스템의 안정성을 높이는 기법입니다.

## 주요 코드 인용

### domain/search_result.py - 검색 결과 모델
```python
# domain/search_result.py:18-34
    def to_dataframe(self) -> pd.DataFrame:
        """
        CSV 저장을 위해 Long format(기사 1건=1행)으로 변환
        """
        data = []
        for i, article in enumerate(self.articles, 1):
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "ai_summary": self.ai_summary
            })
        return pd.DataFrame(data)
```

**코드 설명:**
- `to_dataframe`: 객체 형태의 데이터를 분석이나 저장이 용이한 표(DataFrame) 형태로 변환합니다. 기사별로 행을 나누어 저장하는 'Long format' 방식을 사용합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 2 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│ [원시 데이터] → [유틸리티] → [도메인 객체] │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 3: 서비스 레이어 - API 연동

## 이 프롬프트의 역할
- 외부 API(Tavily 검색, Gemini AI)와 통신하여 실제 비즈니스 가치를 생산하는 기능을 구현합니다.
- 생성된 파일: `services/search_service.py`, `services/ai_service.py`, `utils/exceptions.py`

## 학습 목표
- 외부 라이브러리(SDK)를 활용한 API 연동 패턴 익히기
- API 응답 결과를 목적에 맞게 정렬 및 필터링하는 로직 구현
- 커스텀 예외(`AppError`)를 통한 체계적인 에러 전달 체계 이해

## 이해를 위한 핵심 개념

### 3.1 서비스 레이어 (Service Layer)
애플리케이션의 핵심 비즈니스 로직이 담기는 계층입니다. UI나 데이터베이스와 독립적으로 "검색하기", "요약하기" 등의 기능을 수행합니다.

### 3.2 프롬프트 엔지니어링 (Prompt Engineering)
AI 모델로부터 원하는 형식의 응답을 얻기 위해 질문(프롬프트)을 정교하게 구성하는 과정입니다. 본 프로젝트에서는 한글 요약 및 불릿 포인트 형식을 지정합니다.

## 주요 코드 인용

### services/search_service.py - 뉴스 검색
```python
# services/search_service.py:36-42
            # Tavily 검색 호출
            response = client.search(
                query=keyword,
                search_depth="advanced",
                include_domains=include_domains,
                max_results=max_search_results,
                topic="news"
            )
```

**코드 설명:**
- `TavilyClient`: 검색 엔진 API를 호출합니다. `topic="news"`를 설정하여 뉴스 전용 검색 결과를 가져옵니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 3 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [키워드] → [Tavily API] → [Gemini API] → [요약 결과] │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 4: 리포지토리 레이어 - 데이터 관리

## 이 프롬프트의 역할
- 검색 결과를 파일 시스템(CSV)에 영구적으로 저장하고 불러오는 영속성 계층을 구현합니다.
- 생성된 파일: `repositories/search_repository.py`

## 학습 목표
- `pandas`를 활용한 데이터프레임 조작 및 CSV 입출력 실습
- 파일이 없을 경우 자동 생성하는 방어적 프로그래밍 이해
- 저장된 데이터에서 특정 키로 정보를 다시 재구성하는 역직렬화 기법 이해

## 이해를 위한 핵심 개념

### 4.1 리포지토리 패턴 (Repository Pattern)
데이터 저장소(DB, 파일 등)에 접근하는 로직을 별도 클래스로 분리하여, 다른 코드들이 데이터가 어디에 저장되는지 몰라도 되게 만드는 디자인 패턴입니다.

### 4.2 데이터 영속성 (Persistence)
프로그램이 종료되어도 데이터가 사라지지 않고 유지되는 성질입니다. 본 프로젝트에서는 서버 없이도 운영 가능한 로컬 CSV 파이을 저장소로 사용합니다.

## 주요 코드 인용

### repositories/search_repository.py - 데이터 저장
```python
# repositories/search_repository.py:61-72
    def save(self, search_result: SearchResult) -> bool:
        try:
            new_df = search_result.to_dataframe()
            if os.path.exists(self.csv_path):
                existing_df = self.load()
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                updated_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            else:
                new_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            return True
```

**코드 설명:**
- `pd.concat`: 기존 데이터와 새 데이터를 하나로 합칩니다. `encoding='utf-8-sig'`를 사용하여 엑셀에서 한글이 깨지지 않도록 처리합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 4 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│ [도메인 객체] → [DataFrame] → [CSV 파일] │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 5: UI 컴포넌트

## 이 프롬프트의 역할
- Streamlit을 기반으로 하여 사용자 입력, 사이드바 설정, 결과 표시 등의 독립적인 UI 조각들을 구현합니다.
- 생성된 파일: `components/search_form.py`, `components/sidebar.py`, `components/result_section.py` 등

## 학습 목표
- Streamlit의 위젯(TextInput, Slider, Selectbox 등) 활용법 익히기
- UI 로직을 함수 단위로 모듈화하여 가독성을 높이는 방법 실습
- 에러 및 로딩 상태를 사용자에게 시각적으로 전달하는 인터페이스 설계

## 이해를 위한 핵심 개념

### 5.1 컴포넌트 기반 개발
UI를 재사용 가능한 조각(Component)으로 나누어 개발하는 방식입니다. 이를 통해 코드 복잡도를 줄이고 관리가 용이해집니다.

### 5.2 컨텍스트 매니저 (with 구문)
로딩 스피너와 같이 특정 작업의 시작과 끝을 감싸야 하는 동작을 `with` 구문과 `@contextmanager`를 통해 우아하게 처리합니다.

## 주요 코드 인용

### components/loading.py - 로딩 스피너
```python
# components/loading.py:4-10
@contextmanager
def show_loading(message: str = "뉴스를 검색하고 있습니다..."):
    """
    st.spinner를 context manager로 래핑
    """
    with st.spinner(message):
        yield
```

**코드 설명:**
- `yield`: 이 지점에서 작업을 수행하고, 작업이 끝나면 자동으로 스피너가 사라지게 합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 5 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [사용자 조작] → [컴포넌트 함수] → [화면 출력] │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 6: 메인 앱 통합

## 이 프롬프트의 역할
- 지금까지 만든 모든 레이어(서비스, 리포지토리, 컴포넌트)를 `app.py` 하나에 모아 실제 앱으로 구동시킵니다.
- 생성된 파일: `app.py`

## 학습 목표
- Streamlit의 `session_state`를 통한 애플리케이션 상태 관리 기법 습득
- '검색 모드'와 '기록 조회 모드' 간의 화면 전환 로직 구현
- 전체 시스템 아키텍처 관점에서의 데이터 결합 과정 이해

## 이해를 위한 핵심 개념

### 6.1 세션 상태 (Session State)
Streamlit은 코드 실행 시마다 전체를 재실행하므로, 변수값이 초기화되지 않도록 유지해주는 `st.session_state`가 필수적입니다.

### 6.2 조건부 렌더링
현재 상태(예: 선택된 과거 기록 유무)에 따라 화면에 다른 컴포넌트를 보여주는 기법입니다.

## 주요 코드 인용

### app.py - 메인 실행 루프
```python
# app.py:71-83
    # 검색 실행 로직
    if new_keyword:
        try:
            # 1. 뉴스 검색
            with show_loading(f"🔍 '{new_keyword}' 관련 뉴스를 검색하고 있습니다..."):
                articles = search_news(new_keyword, num_results)
            # ... 중략 ...
            # 2. AI 요약
            with show_loading("🤖 AI가 내용을 분석하고 요약하고 있습니다..."):
                summary = summarize_news(articles)
```

**코드 설명:**
- 서비스 레이어의 함수들을 호출하고, 그 결과를 UI 컴포넌트에 전달하여 최종 화면을 구성합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 6 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│ [사이드바 선택] ──┐                 │
│                   ├→ [메인 제어] → [화면] │
│ [검색 폼 입력] ───┘                 │
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 7: 에러 핸들링 강화 및 마무리

## 이 프롬프트의 역할
- 앱의 안정성을 완성하고 초보자도 쉽게 사용할 수 있도록 가이드 문서(`README.md`)와 상세 에러 처리를 추가합니다.
- 생성된 파일: `README.md`, 업데이트된 `settings.py` 및 서비스 레이어

## 학습 목표
- 사용자 친화적인 에러 메시지(발급 링크 등) 설계의 중요성 인식
- 네트워크 오류 시 자동 재시도 로직 구현을 통한 신뢰성 향상
- 누구나 따라 할 수 있는 상세 설치 설명서 작성 요령 습득

## 이해를 위한 핵심 개념

### 7.1 사용자 중심 에러 설계
단순한 기술적 에러(ValueError)를 넘어서, 사용자가 문제를 스스로 해결할 수 있도록 구체적인 단계(Step-by-step)를 메시지로 제시합니다.

### 7.2 리팩토링 및 문서화
완성된 코드를 다듬고, 타인이 프로젝트를 지속할 수 있도록 표준적인 형태의 문서를 작성하는 과정입니다.

## 주요 코드 인용

### config/settings.py - 상세 안내 에러
```python
# config/settings.py:33-45
            missing_guide = f"""
❌ 환경변수가 설정되지 않았습니다.
누락된 변수: {key}
설정 방법:
1. .env.example 파일을 .env로 복사
2. 각 API 키를 발급받아 .env 파일에 입력
API 키 발급 안내:
- Tavily API: https://tavily.com/
"""
```

**코드 설명:**
- 설정값이 없을 때 링크까지 포함된 상세 텍스트를 제공하여 개발 지식이 적은 사용자도 대응할 수 있게 합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 7 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│ [예외 발생] → [에러 매핑] → [사용자용 안내 메시지] │
│                                     │
└─────────────────────────────────────┘
```

---

# 전체 데이터 흐름

## 시나리오 1: 새로운 키워드 검색 및 요약

```
사용자 키워드 입력
    │
    ▼
utils.preprocess_keyword (입력값 정정 및 제한)
    │
    ▼
services.search_news (Tavily API 연동 및 최신순 정렬)
    │
    ▼
services.ai_service (Gemini API 연동 및 요약 생성)
    │
    ▼
repositories.save (검색 결과 CSV 영구 저장)
    │
    ▼
components.result_section (UI에 결과 표시)
```

## 시나리오 2: 과거 검색 기록 조회

```
사이드바에서 검색 목록 선택
    │
    ▼
repositories.find_by_key (CSV 파일 로드 및 키 필터링)
    │
    ▼
domain.SearchResult 객체 재구성 (CSV 행 데이터를 객체화)
    │
    ▼
components.result_section (저장된 정보 화면 출력)
```

## 폴더 구조 요약

```
TrendTracker/
├── config/       ← [Phase 1, 7] 환경변수 및 API 설정 관리
├── domain/       ← [Phase 2] 데이터 구조 정의 (News, SearchResult)
├── services/     ← [Phase 3, 7] 비즈니스 로직 (검색 엔진, AI 모델 API)
├── repositories/ ← [Phase 4] 데이터 영속성 관리 (CSV 읽기/쓰기)
├── components/   ← [Phase 5] UI 조각들 (폼, 결과창, 사이드바)
├── utils/        ← [Phase 2, 3] 공통 유틸 및 예외 처리
└── app.py        ← [Phase 6] 전체 레이어를 결합하는 앱의 뇌
```

---

## 학습 체크리스트

### Phase 1~2 (기초)
- [ ] `uv`와 `.env`를 이용한 협업 환경 구축을 이해했는가?
- [ ] `dataclass`를 사용하여 데이터 구조를 설계할 수 있는가?

### Phase 3~4 (핵심 로직)
- [ ] 외부 API를 호출하고 응답을 커스터마이징할 수 있는가?
- [ ] 데이터 저장 및 재구성을 위한 리포지토리 패턴을 이해했는가?

### Phase 5~6 (사용자 인터페이스)
- [ ] Streamlit 위젯을 함수화하여 프로젝트에 적용할 수 있는가?
- [ ] 세션 상태를 이용하여 사용자 경험을 관리할 수 있는가?

### Phase 7 (고도화)
- [ ] 예외 케이스를 세밀하게 나누고 사용자에게 친절하게 안내하는가?
- [ ] 타인이 내 도구를 사용할 수 있도록 문서를 정교하게 작성했는가?
