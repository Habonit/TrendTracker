# Step 3: 자료구조

## 학습 목표
- 리스트의 생성, 수정, 삭제, 정렬을 다룬다
- 튜플의 불변성과 집합(set)의 연산을 이해한다
- 딕셔너리로 키-값 데이터를 관리한다

---

## 1. 리스트 (list)

### 리스트란?
여러 개의 값을 **순서대로** 저장하며, 저장된 값을 자유롭게 **추가, 수정, 삭제**할 수 있는 자료구조이다.

| 특징 | 설명 |
|------|------|
| 순서 있음 (ordered) | 인덱스(0부터)로 각 요소에 접근 가능 |
| 변경 가능 (mutable) | 요소를 추가·수정·삭제 가능 |
| 중복 허용 | 같은 값을 여러 번 저장 가능 |
| 다양한 타입 혼합 | 정수, 문자열, 불리언 등을 섞어 담을 수 있음 |

### 리스트 생성

```python
fruits = ["사과", "바나나", "딸기"]     # 대괄호로 생성
empty = []                             # 빈 리스트
chars = list("Python")                 # ['P','y','t','h','o','n']
nums = list(range(1, 6))               # [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None] # 혼합 타입
```

### 인덱싱과 슬라이싱

```python
colors = ["빨강", "주황", "노랑", "초록", "파랑"]

# 인덱싱
colors[0]     # '빨강' (첫 번째)
colors[-1]    # '파랑' (마지막)

# 슬라이싱 [start:end:step] - end는 미포함
colors[:3]    # ['빨강', '주황', '노랑']
colors[2:]    # ['노랑', '초록', '파랑']
colors[::2]   # ['빨강', '노랑', '파랑']
colors[::-1]  # 역순
```

### 주요 메서드 (CRUD)

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `append(x)` | 맨 끝에 요소 추가 | `lst.append(5)` |
| `insert(i, x)` | i 위치에 요소 삽입 | `lst.insert(0, 'a')` |
| `remove(x)` | 값이 x인 첫 번째 요소 제거 | `lst.remove(3)` |
| `pop(i)` | i 위치 요소를 꺼내고 반환 (기본: 마지막) | `lst.pop()` |
| `del lst[i]` | i 위치 요소 삭제 (반환 없음) | `del lst[2]` |

```python
animals = ["고양이", "강아지", "토끼"]
animals.append("햄스터")           # 추가
animals.insert(1, "앵무새")        # 삽입
animals[0] = "페르시안 고양이"      # 수정
animals.remove("앵무새")           # 값으로 삭제
removed = animals.pop()            # 마지막 요소 꺼내기
del animals[0]                     # 인덱스로 삭제
```

### 정렬: sort() vs sorted()

```python
scores = [85, 92, 78, 95, 88]

# sorted(): 새 리스트 반환 (원본 유지)
sorted_scores = sorted(scores)
desc_scores = sorted(scores, reverse=True)

# sort(): 원본 자체를 정렬 (반환값 None)
scores.sort()

# reverse(): 순서 뒤집기
scores.reverse()
```

> **핵심 차이**: `sort()`는 원본 변경 + 반환 None, `sorted()`는 원본 유지 + 새 리스트 반환

### 기타 유용한 기능

```python
items = ["연필", "지우개", "자"]
len(items)           # 3 (길이)
"연필" in items      # True (포함 여부)
"볼펜" not in items  # True (미포함 여부)
```

### 중첩 리스트

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
matrix[0]       # [1, 2, 3]  (첫 번째 행)
matrix[1][2]    # 6          (2행 3열)
```

---

## 2. 튜플 (tuple)

### 튜플이란?
리스트와 비슷하지만, 한 번 만들면 **변경할 수 없는(immutable)** 자료구조이다.

| 구분 | 리스트 `[]` | 튜플 `()` |
|------|-------------|----------|
| 변경 가능 여부 | 가능 (mutable) | 불가능 (immutable) |
| 기호 | 대괄호 `[]` | 소괄호 `()` |
| 속도 | 상대적으로 느림 | 상대적으로 빠름 |
| 용도 | 수정이 필요한 데이터 | 수정이 불필요한 고정 데이터 |

### 튜플 생성과 사용

```python
point = (3, 5)
colors = ("빨강", "초록", "파랑")
single = (42,)   # 요소가 하나인 튜플 → 쉼표 필수!
not_tuple = (42)  # 이건 그냥 정수 42

colors[0]   # '빨강' (인덱싱은 가능)
colors[0] = "노랑"  # TypeError! (수정 불가)
```

### 패킹과 언패킹

```python
# 패킹: 여러 값을 튜플로 묶기
person = "홍길동", 25, "서울"  # 괄호 없이도 가능

# 언패킹: 튜플을 여러 변수에 풀기
name, age, city = person

# 일부만 받고 나머지는 *로 묶기
first, *rest = (1, 2, 3, 4, 5)  # first=1, rest=[2,3,4,5]
```

### 함수에서 다중 반환값

```python
def min_max(numbers):
    return min(numbers), max(numbers)  # 튜플로 반환

minimum, maximum = min_max([45, 78, 23, 91])  # 언패킹으로 받기
```

### 튜플의 활용
- 좌표 `(x, y)`, 색상 `(R, G, B)` 등 고정된 묶음 데이터
- 함수에서 여러 값을 동시에 반환할 때
- 딕셔너리의 키로 사용 (리스트는 불가능)

---

## 3. 집합 (set)

### 집합이란?
수학의 집합과 동일한 개념으로, **중복을 허용하지 않고** **순서가 없는** 자료구조이다.

| 특징 | 설명 |
|------|------|
| 중복 없음 | 같은 값을 여러 번 넣어도 하나만 유지 |
| 순서 없음 | 인덱싱으로 접근 불가 |
| 집합 연산 지원 | 합집합, 교집합, 차집합 등 |

### 집합 생성과 조작

```python
fruits = {"사과", "바나나", "딸기", "사과"}  # 중복 자동 제거
empty_set = set()  # 빈 집합 ({}는 빈 딕셔너리!)

fruits.add("키위")        # 추가
fruits.remove("바나나")   # 삭제 (없으면 에러)
fruits.discard("호랑이")  # 삭제 (없어도 에러 안남)
```

### 집합 연산

| 연산 | 연산자 | 메서드 | 설명 |
|------|--------|--------|------|
| 합집합 | `A \| B` | `A.union(B)` | A 또는 B에 있는 모든 요소 |
| 교집합 | `A & B` | `A.intersection(B)` | A와 B 모두에 있는 요소 |
| 차집합 | `A - B` | `A.difference(B)` | A에만 있는 요소 |
| 대칭차집합 | `A ^ B` | `A.symmetric_difference(B)` | A 또는 B 중 하나에만 있는 요소 |

```python
music = {"지민", "수현", "태영", "하은"}
art = {"수현", "채린", "태영", "민서"}

music | art   # 합집합: 둘 중 하나라도 속한 멤버
music & art   # 교집합: {'수현', '태영'}
music - art   # 차집합: 음악만
music ^ art   # 대칭차집합: 하나에만 속한 멤버
```

### 리스트 중복 제거에 활용

```python
scores = [85, 92, 78, 85, 92, 100, 78]
unique = list(set(scores))  # 중복 제거
```

---

## 4. 딕셔너리 (dict)

### 딕셔너리란?
**키(key)** 와 **값(value)** 의 쌍으로 데이터를 저장하는 자료구조이다.

| 특징 | 설명 |
|------|------|
| 키-값 쌍 | 각 데이터는 `key: value` 형태 |
| 키 중복 불가 | 같은 키가 두 번 나오면 마지막 값으로 덮어씀 |
| 키는 불변 타입 | 문자열, 숫자, 튜플 가능 / 리스트, 집합 불가 |
| 변경 가능 | 생성 후 추가, 수정, 삭제 가능 |
| 순서 유지 | Python 3.7+부터 삽입 순서 유지 |

### 생성과 접근

```python
student = {
    "이름": "김지수",
    "나이": 20,
    "전공": "컴퓨터공학"
}
student["이름"]           # '김지수' (없으면 KeyError)
student.get("전화", "미등록")  # '미등록' (없으면 기본값 반환)
```

### CRUD (추가/수정/삭제)

```python
book = {"제목": "파이썬 입문", "저자": "홍길동", "가격": 25000}

# 추가
book["출판사"] = "한빛미디어"

# 수정
book["가격"] = 28000

# 삭제
del book["출판사"]                    # del: 삭제만
publisher = book.pop("출판사", "없음") # pop: 삭제 + 값 반환 (기본값 지정 가능)
```

### 딕셔너리 순회

```python
scores = {"국어": 90, "영어": 85, "수학": 92}

for subject in scores.keys():       # 키만 순회
    print(subject)

for score in scores.values():       # 값만 순회
    print(score)

for subject, score in scores.items():  # 키-값 쌍 순회 (가장 많이 사용)
    print(f"{subject}: {score}점")
```

### get() vs [] 차이

```python
user = {"이름": "박민수"}

user["전화"]                   # KeyError!
user.get("전화")               # None
user.get("전화", "미등록")      # "미등록"
```

> `get()`은 키가 없을 때 에러 없이 안전하게 처리할 수 있다.

### 중첩 딕셔너리

```python
students = {
    "S001": {
        "이름": "김지수",
        "성적": {"국어": 90, "영어": 85, "수학": 92}
    }
}
students["S001"]["성적"]["수학"]  # 92
```

### 딕셔너리 컴프리헨션

```python
squares = {n: n**2 for n in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 두 리스트를 딕셔너리로 합치기 (zip 활용)
keys = ["이름", "나이", "도시"]
values = ["홍길동", 25, "서울"]
person = dict(zip(keys, values))
```

---

## 실습 문제

### 실습 1: 과일 리스트 CRUD 관리

1. `["사과", "바나나", "딸기"]` 리스트를 만드세요
2. `"포도"`를 맨 뒤에 추가
3. `"키위"`를 인덱스 1에 삽입
4. `"바나나"`를 삭제
5. 가나다순 정렬
6. 최종 리스트와 길이 출력
7. `"망고"` 포함 여부 확인

```python
fruits = ["사과", "바나나", "딸기"]
fruits.append("포도")
fruits.insert(1, "키위")
fruits.remove("바나나")
fruits.sort()
print(f"최종: {fruits}, 길이: {len(fruits)}")
print(f"'망고' 포함 여부: {'망고' in fruits}")
```

---

### 실습 2: 튜플 활용과 리스트 중복 제거

**문제 1**: 세 점의 좌표를 튜플로 만들고, 언패킹하여 x/y 좌표 평균을 구하세요.

```python
A, B, C = (1, 2), (4, 6), (7, 3)
ax, ay = A
bx, by = B
cx, cy = C
avg_x = (ax + bx + cx) / 3
avg_y = (ay + by + cy) / 3
print(f"x평균: {avg_x:.1f}, y평균: {avg_y:.1f}")
```

**문제 2**: 리스트 `[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]`에서 중복 제거 후 오름차순 정렬

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
unique_sorted = sorted(set(numbers))
print(f"중복 제거 + 정렬: {unique_sorted}")
```

---

### 실습 3: 전화번호부 만들기

딕셔너리를 활용하여 연락처 등록, 추가, 수정, 검색, 삭제, 전체 출력을 수행하세요.

```python
phonebook = {
    "김민수": "010-1234-5678",
    "이지영": "010-9876-5432",
    "박현우": "010-5555-1234"
}

phonebook["최수현"] = "010-7777-8888"              # 추가
phonebook["김민수"] = "010-1111-2222"              # 수정
print(phonebook.get("이지영", "등록되지 않음"))      # 검색
print(phonebook.get("홍길동", "등록되지 않음"))      # 없는 이름 검색
del phonebook["박현우"]                            # 삭제

for name, number in phonebook.items():
    print(f"  {name}: {number}")
```

---

## 핵심 요약: 자료구조 비교

| 자료구조 | 기호 | 순서 | 변경 | 중복 | 주요 용도 |
|----------|------|------|------|------|----------|
| **리스트** | `[]` | O | O | O | 순서가 있는 데이터 모음 |
| **튜플** | `()` | O | X | O | 변경 불필요한 고정 데이터 |
| **집합** | `{}` | X | O | X | 중복 제거, 집합 연산 |
| **딕셔너리** | `{k:v}` | O* | O | 키 X | 키-값 매핑 데이터 |

\* Python 3.7+부터 삽입 순서 유지
