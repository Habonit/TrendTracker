# Step 1: 기초 문법

## 학습 목표
- 변수를 선언하고 다양한 자료형을 이해한다
- 산술, 비교, 논리 연산자를 활용한다
- 문자열 인덱싱, 슬라이싱, f-string을 다룬다
- `print()`와 `input()`으로 입출력을 처리한다

---

## 1. 변수와 자료형

### 변수란?
변수(variable)는 **데이터를 저장하는 이름이 붙은 공간**이다.
파이썬에서는 `=` 기호를 사용해 변수에 값을 할당한다.

```python
age = 25          # 정수(int)
height = 175.5    # 실수(float)
name = "홍길동"    # 문자열(str)
is_student = True # 불리언(bool)
```

### 기본 자료형 4가지

| 자료형 | 키워드 | 설명 | 예시 |
|--------|--------|------|------|
| 정수 | `int` | 소수점 없는 숫자 | `10`, `-3`, `0` |
| 실수 | `float` | 소수점 있는 숫자 | `3.14`, `-0.5` |
| 문자열 | `str` | 텍스트 데이터 | `"hello"`, `'파이썬'` |
| 불리언 | `bool` | 참/거짓 | `True`, `False` |

### 핵심 함수
- `type()` : 변수의 자료형을 확인
- `int()`, `float()`, `str()`, `bool()` : 형변환 함수

### 형변환 (Type Casting)

```python
int(3.7)       # 3   (소수점 버림, 반올림 아님!)
int("42")      # 42  (문자열 → 정수)
float(10)      # 10.0
str(100)       # '100'
bool(0)        # False (0은 False, 나머지는 True)
bool("")       # False (빈 문자열은 False)
bool(None)     # False
```

### 변수 이름 규칙
- 영문자, 숫자, `_` 사용 가능 (숫자로 시작 불가)
- 대소문자 구분 (`name` ≠ `Name`)
- 예약어 사용 불가 (`if`, `for`, `class` 등)
- 권장 스타일: `snake_case` (예: `user_name`, `total_count`)
- 상수는 대문자로 (관례): `MAX_SIZE = 1000`

---

## 2. 연산자

### 산술 연산자

| 연산자 | 설명 | 예시 | 결과 |
|--------|------|------|------|
| `+` | 덧셈 | `7 + 3` | `10` |
| `-` | 뺄셈 | `7 - 3` | `4` |
| `*` | 곱셈 | `7 * 3` | `21` |
| `/` | 나눗셈 | `7 / 3` | `2.333...` |
| `//` | 몫 (정수 나눗셈) | `7 // 3` | `2` |
| `%` | 나머지 | `7 % 3` | `1` |
| `**` | 거듭제곱 | `2 ** 3` | `8` |

> `/` 나눗셈은 항상 `float`을 반환한다.

### 비교 연산자 (결과: True / False)

| 연산자 | 설명 | 예시 | 결과 |
|--------|------|------|------|
| `==` | 같다 | `5 == 5` | `True` |
| `!=` | 다르다 | `5 != 3` | `True` |
| `<` | 작다 | `3 < 5` | `True` |
| `>` | 크다 | `3 > 5` | `False` |
| `<=` | 작거나 같다 | `5 <= 5` | `True` |
| `>=` | 크거나 같다 | `3 >= 5` | `False` |

### 논리 연산자

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `and` | 둘 다 True여야 True | `True and False` → `False` |
| `or` | 하나라도 True이면 True | `True or False` → `True` |
| `not` | 반대로 뒤집기 | `not True` → `False` |

### 할당 연산자 (단축 표현)

| 연산자 | 동일 표현 |
|--------|----------|
| `x += 3` | `x = x + 3` |
| `x -= 3` | `x = x - 3` |
| `x *= 3` | `x = x * 3` |
| `x /= 3` | `x = x / 3` |

---

## 3. 문자열 다루기

### 인덱싱 (Indexing)

문자열의 각 문자에는 번호(인덱스)가 있다. 파이썬의 인덱스는 **0부터** 시작한다.

```
문자열:  P  y  t  h  o  n
인덱스:  0  1  2  3  4  5
음수:   -6 -5 -4 -3 -2 -1
```

```python
text = "Python"
text[0]    # 'P'  (첫 번째)
text[-1]   # 'n'  (마지막)
len(text)  # 6    (길이)
```

### 슬라이싱 (Slicing)

문자열의 일부분을 잘라내는 기능이다. `문자열[시작:끝:간격]` 형식을 사용한다.
**끝 인덱스는 포함되지 않는다!**

```python
text = "Hello, Python!"
text[0:5]    # 'Hello'
text[7:]     # 'Python!'
text[:5]     # 'Hello'
text[::2]    # 'Hlo yhn'  (한 글자씩 건너뛰기)
text[::-1]   # '!nohtyP ,olleH'  (역순)
```

### f-string (Formatted String Literal)

문자열 안에 변수를 직접 넣을 수 있는 편리한 문법이다.

```python
name = "김철수"
age = 28
score = 95.678

print(f"이름: {name}, 나이: {age}세")
print(f"내년 나이: {age + 1}세")      # 식 포함 가능
print(f"점수: {score:.1f}")           # 소수점 1자리: 95.7
print(f"번호: {42:05d}")              # 0 채우기: 00042
print(f"가격: {1500000:,}원")         # 천단위 콤마: 1,500,000원
```

### 주요 문자열 메서드

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `upper()` / `lower()` | 대소문자 변환 | `"Hello".upper()` → `"HELLO"` |
| `strip()` | 양쪽 공백 제거 | `" hi ".strip()` → `"hi"` |
| `split(구분자)` | 문자열 분리 → 리스트 | `"a,b,c".split(",")` → `['a','b','c']` |
| `join(리스트)` | 리스트 → 문자열 결합 | `"-".join(['a','b'])` → `"a-b"` |
| `replace(old, new)` | 문자열 교체 | `"Java".replace("Java","Python")` |
| `find(문자열)` | 위치 찾기 (없으면 -1) | `"hello".find("ll")` → `2` |
| `count(문자열)` | 등장 횟수 | `"banana".count("a")` → `3` |
| `startswith()` / `endswith()` | 시작/끝 확인 | `"file.py".endswith(".py")` → `True` |

---

## 4. 입출력

### print() 함수
```python
print("Hello!")                              # 기본 출력
print("A", "B", "C", sep="-")               # 구분자: A-B-C
print("로딩", end="...")                      # 줄바꿈 대신 "..."
print(f"{name}님의 점수: {score}점")          # f-string 출력
```

### input() 함수
- `input()`의 반환값은 **항상 문자열(str)**
- 숫자로 사용하려면 **형변환 필요**

```python
name = input("이름을 입력하세요: ")          # 문자열 그대로
age = int(input("나이를 입력하세요: "))       # 정수 변환
height = float(input("키를 입력하세요: "))    # 실수 변환
```

---

## 실습 문제

### 실습 1: 다양한 자료형 변수 만들기
다음 요구사항에 맞는 변수를 선언하고, `type()`으로 자료형을 확인해 보세요.

1. 정수형 변수 `score`에 점수 저장
2. 실수형 변수 `temperature`에 온도 저장
3. 문자열 변수 `city`에 도시 이름 저장
4. 불리언 변수 `is_raining`에 날씨 상태 저장
5. `temperature`를 정수로 형변환하여 출력

```python
# 예시 정답
score = 95
temperature = 23.5
city = "서울"
is_raining = False

print(f"score = {score}, 자료형: {type(score)}")
print(f"temperature = {temperature}, 자료형: {type(temperature)}")
print(f"city = {city}, 자료형: {type(city)}")
print(f"is_raining = {is_raining}, 자료형: {type(is_raining)}")
print(f"temperature 정수 변환: {int(temperature)}")
```

---

### 실습 2: 연산자별 결과 예측
아래 식들의 결과를 **먼저 예측**한 뒤, 코드를 실행해서 확인해 보세요.

1. `15 // 4` → ?
2. `15 % 4` → ?
3. `2 ** 10` → ?
4. `10 > 5 and 3 > 7` → ?
5. `not (5 == 5)` → ?

```python
# 정답: 3, 3, 1024, False, False
```

---

### 실습 3: 문자열 조작 연습

1. `"  hello, WORLD!  "`를 공백 제거 후 소문자로 변환
2. `"2024-01-15"`에서 년도, 월, 일을 각각 변수에 저장 (`split` 사용)
3. `"apple banana cherry"`에서 `"banana"`를 `"mango"`로 교체
4. `"programming"`의 3번째부터 7번째 문자까지 슬라이싱

```python
# 1
text1 = "  hello, WORLD!  "
print(text1.strip().lower())  # 'hello, world!'

# 2
date = "2024-01-15"
year, month, day = date.split("-")
print(f"년: {year}, 월: {month}, 일: {day}")

# 3
fruits = "apple banana cherry"
print(fruits.replace("banana", "mango"))

# 4
word = "programming"
print(word[2:7])  # 'ogram'
```

---

### 실습 4: input으로 이름/나이 받아 출력하기
`input()`으로 이름과 나이를 입력받아서 아래와 같이 출력하세요.

```
===== 개인 정보 =====
이름: 홍길동
나이: 25세
태어난 해: 2001년
==================
```

```python
name = input("이름을 입력하세요: ")
age = int(input("나이를 입력하세요: "))
birth_year = 2026 - age

print("===== 개인 정보 =====")
print(f"이름: {name}")
print(f"나이: {age}세")
print(f"태어난 해: {birth_year}년")
print("==================")
```

---

## 핵심 요약

| 주제 | 핵심 키워드 |
|------|-------------|
| **변수와 자료형** | `int`, `float`, `str`, `bool`, `type()`, 형변환 함수 |
| **연산자** | `+`, `-`, `*`, `/`, `//`, `%`, `**`, `==`, `!=`, `and`, `or`, `not`, `+=` |
| **문자열** | 인덱싱, 슬라이싱, f-string, `upper()`, `lower()`, `strip()`, `split()`, `join()`, `replace()` |
| **입출력** | `print(sep, end)`, `input()`, 형변환 조합 |
