## Phase 4: 리포지토리 레이어 - 데이터 관리 (7단계 중 4단계)

---

Phase 4: CSV 데이터 관리를 위한 리포지토리를 구현합니다.

### repositories/search_repository.py

#### CSV 데이터 구조 (8개 컬럼)

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| search_key | string | PK, "키워드-yyyymmddhhmm" |
| search_time | datetime | 검색 실행 시간 |
| keyword | string | 검색 키워드 |
| article_index | int | 기사 순번 (1부터) |
| title | string | 기사 제목 |
| url | string | 기사 URL |
| snippet | string | 기사 스니펫 |
| ai_summary | string | AI 요약 결과 |

---

### SearchRepository 클래스

#### 초기화
- `__init__(self, csv_path: str)`
- csv_path는 config.settings에서 가져옴

#### `load() -> pd.DataFrame`
- CSV 파일 존재 시: `pandas.read_csv()`로 로드
- 파일 부재 시: 8개 컬럼의 빈 DataFrame 반환
- 파일 읽기 실패 시: 경고 로그 후 빈 DataFrame 반환

#### `save(search_result: SearchResult) -> bool`
- SearchResult의 `to_dataframe()` 메서드로 DataFrame 변환
- 기존 데이터에 append
- `df.to_csv(csv_path, index=False)`
- 성공 시 True, 실패 시 False 반환

#### `get_all_keys() -> List[str]`
- search_key 컬럼의 고유값 리스트 반환
- search_time 기준 최신순 정렬

#### `find_by_key(search_key: str) -> Optional[SearchResult]`
- search_key로 필터링
- SearchResult 객체로 재구성하여 반환
- 없으면 None

#### `get_all_as_csv() -> str`
- 전체 DataFrame을 CSV 문자열로 반환
- `st.download_button`에서 사용

---

### 예외 처리
- 파일 읽기/쓰기 실패 시 `AppError("file_error")` raise하지 않고 graceful 처리
- 로그로 에러 기록
- data/ 폴더가 없으면 자동 생성되도록 처리

---

### ⚠️ CSV 저장소 관련 사용자 알림 (UI에 표시)

앱 사이드바 또는 설정 영역에 다음 주의사항을 표시해주세요:

```
💾 데이터 저장 안내
- 검색 기록은 CSV 파일(data/search_history.csv)에 저장됩니다.
- CSV 파일을 삭제하거나 경로를 변경하면 이전 검색 기록이 모두 사라집니다.
- 중요한 기록은 CSV 다운로드 기능을 통해 백업해주세요.
```

이 안내문은 `components/sidebar.py`의 `render_info()` 함수 내 "ℹ️ 사용법" 섹션 또는 별도 expander로 구현해주세요.

---

### 구현 요구사항
- pandas 라이브러리 사용
- 타입 힌트 명확히 작성
- `os.makedirs(exist_ok=True)`로 폴더 자동 생성

---

### 검증 방법

```bash
# 리포지토리 import 테스트
python -c "from repositories.search_repository import SearchRepository; print('SearchRepository import 성공')"

# 리포지토리 기본 동작 테스트
python -c "
from repositories.search_repository import SearchRepository
repo = SearchRepository('data/search_history.csv')
df = repo.load()
print(f'컬럼: {list(df.columns)}')
print(f'행 수: {len(df)}')
"
```

---

### 검증 포인트

- [ ] `from repositories.search_repository import SearchRepository` import 성공
- [ ] `data/` 폴더 자동 생성 확인
- [ ] `load()` 실행 시 8개 컬럼의 DataFrame 반환
- [ ] `save()` 후 CSV 파일 생성 확인
- [ ] `get_all_keys()` 최신순 정렬 확인
- [ ] `find_by_key()` 정상 동작 확인
- [ ] `get_all_as_csv()` CSV 문자열 반환 확인

---

---

### ⚠️ 필수 요구사항: 한글 사용

**모든 UI 텍스트와 사용자에게 보여지는 메시지는 반드시 한글로 작성해주세요:**
- 로그 메시지
- 에러 안내
- 상태 메시지

예시:
- ❌ "File not found"
- ✅ "파일을 찾을 수 없습니다"

---

### 🚫 금지사항: Git/GitHub 작업 금지

**Git 및 GitHub 관련 작업은 일절 하지 마세요.**