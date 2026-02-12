# Step 4: 함수와 모듈

## 학습 목표
- 함수를 정의하고 매개변수/반환값을 활용한다
- 스코프를 이해하고 lambda 함수를 사용한다
- 모듈과 표준 라이브러리를 활용한다

---

## 1. 함수 정의

### 함수란?
함수는 **특정 작업을 수행하는 코드 묶음**이다. `def` 키워드로 정의한다.

### 기본 구조

```python
def 함수이름(매개변수1, 매개변수2):
    """독스트링: 함수 설명"""
    # 함수 본문
    return 반환값
```

### 기본 함수 정의와 호출

```python
def greet(name):
    """인사 메시지를 반환하는 함수"""
    return f"안녕하세요, {name}님!"

print(greet("파이썬"))  # 안녕하세요, 파이썬님!

# return이 없는 함수 → None 반환
def say_hello():
    print("Hello!")

result = say_hello()
print(result)  # None
```

### 매개변수 종류

| 종류 | 설명 | 예시 |
|------|------|------|
| 위치 매개변수 | 순서대로 전달 | `def f(a, b)` |
| 기본값 매개변수 | 기본값 지정 | `def f(a, b=10)` |
| `*args` | 가변 위치 인자 (튜플로 받음) | `def f(*args)` |
| `**kwargs` | 가변 키워드 인자 (딕셔너리로 받음) | `def f(**kwargs)` |

### 기본값 매개변수와 키워드 인자

```python
def introduce(name, age, city="서울"):
    return f"{name}님, {age}세, {city} 거주"

introduce("홍길동", 25)                # city 기본값 사용
introduce("김철수", 30, "부산")        # 기본값 변경
introduce(age=28, name="이영희")       # 키워드 인자 (순서 무관)
```

### *args와 **kwargs

```python
# *args: 여러 개의 위치 인자를 튜플로 받음
def total(*args):
    print(f"args = {args}")   # (1, 2, 3, 4, 5)
    return sum(args)

total(1, 2, 3, 4, 5)  # 15

# **kwargs: 여러 개의 키워드 인자를 딕셔너리로 받음
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

show_info(이름="홍길동", 나이=25, 도시="서울")
```

### 다중 반환값 (튜플)

```python
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(f"최솟값: {lo}, 최댓값: {hi}")
```

### docstring 작성

```python
def calculate_bmi(weight, height):
    """
    BMI(체질량지수)를 계산합니다.

    Args:
        weight (float): 몸무게 (kg)
        height (float): 키 (m)

    Returns:
        float: BMI 값
    """
    return weight / (height ** 2)

help(calculate_bmi)  # docstring 확인
```

---

## 2. 스코프와 람다

### 변수 스코프 (Scope)

- **지역 변수**: 함수 안에서 정의, 함수 안에서만 사용 가능
- **전역 변수**: 함수 바깥에서 정의, 어디서든 읽기 가능
- `global` 키워드: 함수 안에서 전역 변수를 수정할 때 사용

```python
x = 10  # 전역 변수

def my_func():
    x = 20  # 지역 변수 (전역 x와 다른 변수)
    print(f"함수 내부 x = {x}")   # 20

my_func()
print(f"함수 외부 x = {x}")      # 10 (전역 x는 변하지 않음)

# global 키워드로 전역 변수 수정
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)  # 2
```

### lambda 함수

한 줄짜리 **익명 함수**이다.

```python
# 기본 문법: lambda 매개변수: 표현식
square = lambda x: x ** 2
print(square(5))  # 25
```

### map, filter, sorted와 함께 사용

| 함수 | 설명 | 예시 |
|------|------|------|
| `map(func, iterable)` | 모든 요소에 함수 적용 | `map(lambda x: x**2, [1,2,3])` |
| `filter(func, iterable)` | 조건이 True인 요소만 | `filter(lambda x: x%2==0, [1,2,3])` |
| `sorted(iterable, key=func)` | key 기준 정렬 | `sorted(words, key=len)` |

```python
numbers = [1, 2, 3, 4, 5]

# map: 모든 요소에 함수 적용
squared = list(map(lambda x: x ** 2, numbers))  # [1, 4, 9, 16, 25]

# filter: 조건에 맞는 요소만
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# sorted with key
words = ["banana", "apple", "cherry", "date"]
by_length = sorted(words, key=lambda w: len(w))  # 길이순 정렬

# 딕셔너리 리스트 정렬
students = [
    {"name": "홍길동", "score": 85},
    {"name": "김철수", "score": 92},
    {"name": "이영희", "score": 78},
]
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
```

---

## 3. 모듈과 패키지

### import 방법

```python
import math              # 모듈 전체
from math import sqrt    # 특정 함수만
import numpy as np       # 별칭 사용
```

### 주요 표준 라이브러리

#### math 모듈 - 수학 함수

```python
import math

math.pi            # 3.141592653589793
math.e             # 2.718281828459045
math.sqrt(16)      # 4.0
math.ceil(3.2)     # 4  (올림)
math.floor(3.8)    # 3  (내림)
math.factorial(5)  # 120
```

#### random 모듈 - 난수 생성

```python
import random

random.randint(1, 6)                    # 1~6 범위 랜덤 정수
random.choice(["짜장", "짬뽕", "볶음밥"])  # 리스트에서 랜덤 선택
random.sample(range(1, 46), 6)          # 중복 없이 여러 개 선택
random.shuffle(cards)                   # 리스트 섞기 (원본 변경)
```

#### datetime 모듈 - 날짜/시간

```python
from datetime import datetime, timedelta

now = datetime.now()                                    # 현재 시각
now.strftime('%Y년 %m월 %d일 %H:%M')                    # 포맷 출력
week_later = now + timedelta(days=7)                    # 7일 후
birthday = datetime(2000, 1, 15)                        # 특정 날짜
age_days = (now - birthday).days                         # 날짜 차이 (일수)
```

---

## 실습 문제

### 실습 1: 사칙연산 함수 작성

add, subtract, multiply, divide 4개 함수를 작성하세요. divide는 0으로 나누기를 처리해야 합니다.

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "0으로 나눌 수 없습니다"
    return a / b

print(f"10 + 3 = {add(10, 3)}")
print(f"10 - 3 = {subtract(10, 3)}")
print(f"10 * 3 = {multiply(10, 3)}")
print(f"10 / 3 = {divide(10, 3):.2f}")
print(f"10 / 0 = {divide(10, 0)}")
```

---

### 실습 2: lambda + map으로 섭씨→화씨 변환

```python
celsius = [0, 10, 20, 30, 40, 100]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))

for c, f in zip(celsius, fahrenheit):
    print(f"{c}°C = {f}°F")
```

---

### 실습 3: 표준 라이브러리 활용

```python
import math, random
from datetime import datetime

# 1. 원의 넓이 (반지름 = 5)
r = 5
area = math.pi * r ** 2
print(f"반지름 {r}인 원의 넓이: {area:.2f}")

# 2. 1~100 사이 랜덤 수 5개
randoms = [random.randint(1, 100) for _ in range(5)]
print(f"랜덤 수: {randoms}")

# 3. 크리스마스까지 남은 일수
now = datetime.now()
christmas = datetime(now.year, 12, 25)
if christmas < now:
    christmas = datetime(now.year + 1, 12, 25)
days_left = (christmas - now).days
print(f"크리스마스까지 {days_left}일 남음")
```

---

## 핵심 요약

| 개념 | 핵심 내용 |
|------|----------|
| **함수 정의** | `def`, 매개변수, `return`, 기본값, `*args`, `**kwargs` |
| **스코프** | 지역/전역 변수, `global` 키워드 |
| **lambda** | `lambda x: x**2`, `map()`, `filter()`, `sorted(key=)` |
| **모듈** | `import`, `from...import`, `math`, `random`, `datetime` |
