# Step 2: 제어문과 반복문

## 학습 목표
- if/elif/else 조건문을 활용하여 프로그램 흐름을 제어한다
- for, while 반복문으로 반복 작업을 수행한다
- 리스트 컴프리헨션으로 간결한 코드를 작성한다

---

## 1. 조건문 (if / elif / else)

### 기본 구조

```python
if 조건식:
    # 조건이 True일 때 실행
elif 다른_조건식:
    # 첫 번째 조건이 False이고, 이 조건이 True일 때 실행
else:
    # 모든 조건이 False일 때 실행
```

> Python은 **들여쓰기(4칸)**로 코드 블록을 구분한다. 들여쓰기가 맞지 않으면 `IndentationError`가 발생한다.

### 조건문 예시: 학점 판정

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"점수: {score}점 -> 학점: {grade}")
```

### 중첩 조건문

if 문 안에 또 다른 if 문을 넣을 수 있다.

```python
age = 25
has_id = True

if age >= 19:
    if has_id:
        print("입장 가능합니다.")
    else:
        print("신분증이 필요합니다.")
else:
    print("미성년자는 입장할 수 없습니다.")
```

논리 연산자로 더 간결하게 표현할 수도 있다:

```python
if age >= 19 and has_id:
    print("입장 가능합니다.")
```

### 삼항 연산자 (Conditional Expression)

한 줄로 조건을 표현할 수 있다.

```python
# 값A if 조건 else 값B
weather = "더움" if temperature >= 30 else "적당함"
status = "성인" if age >= 19 else "미성년"
result = "짝수" if num % 2 == 0 else "홀수"
```

### 논리 연산자 정리

| 연산자 | 의미 | 예시 |
|--------|------|------|
| `and` | 두 조건 모두 True | `x > 0 and x < 10` |
| `or` | 둘 중 하나라도 True | `x < 0 or x > 100` |
| `not` | 조건을 반전 | `not is_empty` |

---

## 2. 반복문 (for / while)

### for 문

시퀀스(iterable)의 각 요소를 하나씩 순회한다.

```python
for 변수 in 시퀀스:
    # 반복할 코드
```

```python
fruits = ["사과", "바나나", "딸기"]
for fruit in fruits:
    print(fruit)

# 문자열도 순회 가능
for char in "Python":
    print(char, end=" ")  # P y t h o n
```

### range() 함수

| 형태 | 설명 | 예시 |
|------|------|------|
| `range(n)` | 0부터 n-1까지 | `range(5)` → 0, 1, 2, 3, 4 |
| `range(start, stop)` | start부터 stop-1까지 | `range(2, 7)` → 2, 3, 4, 5, 6 |
| `range(start, stop, step)` | start부터 stop-1까지 step 간격 | `range(0, 20, 3)` → 0, 3, 6, 9, 12, 15, 18 |

```python
# 역순
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### while 문

조건이 True인 동안 계속 반복한다.

```python
while 조건식:
    # 반복할 코드
    # 조건을 변경하는 코드 (없으면 무한 루프!)
```

```python
count = 1
while count <= 5:
    print(f"현재 카운트: {count}")
    count += 1
```

### break와 continue

- `break` : 반복문을 즉시 종료
- `continue` : 현재 순회를 건너뛰고 다음 순회로

```python
# break: 7을 찾으면 중단
for num in [3, 1, 4, 1, 5, 9, 7, 6]:
    if num == 7:
        print("7을 찾았습니다!")
        break
    print(f"확인 중: {num}")

# continue: 홀수 건너뛰고 짝수만 출력
for i in range(1, 11):
    if i % 2 != 0:
        continue
    print(f"짝수: {i}")
```

### enumerate()

인덱스와 값을 함께 순회한다.

```python
students = ["김철수", "이영희", "박지민"]

# 기본 사용
for idx, student in enumerate(students):
    print(f"{idx + 1}번: {student}")

# start 매개변수로 시작 번호 지정
for idx, student in enumerate(students, start=1):
    print(f"{idx}번: {student}")
```

### for vs while 선택 기준

| 상황 | 추천 |
|------|------|
| 반복 횟수가 정해져 있을 때 | `for` |
| 리스트/문자열 등을 순회할 때 | `for` |
| 종료 조건은 있지만 횟수를 모를 때 | `while` |
| 사용자 입력을 반복 받을 때 | `while` |

### 중첩 반복문 예시: 구구단

```python
for dan in range(2, 4):
    print(f"\n=== {dan}단 ===")
    for i in range(1, 10):
        print(f"{dan} x {i} = {dan * i}")
```

---

## 3. 리스트 컴프리헨션 (List Comprehension)

리스트를 간결하게 생성하는 문법이다.

### 기본 문법

```python
[표현식 for 변수 in 시퀀스]              # 기본
[표현식 for 변수 in 시퀀스 if 조건]      # 조건부 필터링
```

### for문과의 비교

```python
# for문 버전
squares = []
for i in range(1, 11):
    squares.append(i ** 2)

# 컴프리헨션 버전 (동일한 결과)
squares = [i ** 2 for i in range(1, 11)]
```

### 조건부 컴프리헨션

```python
# 짝수만 추출
evens = [n for n in range(1, 21) if n % 2 == 0]

# 3의 배수의 제곱
result = [x ** 2 for x in range(1, 11) if x % 3 == 0]
```

### 다양한 활용 예시

```python
# 대문자 변환
words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]

# 삼항 연산자와 조합
signs = ["양수" if n > 0 else "음수" for n in [-3, -1, 0, 2, 5]]

# 중첩 컴프리헨션 (좌표 조합)
pairs = [(x, y) for x in range(1, 4) for y in range(1, 4)]
```

### 주의 사항
- 너무 복잡한 컴프리헨션은 가독성을 떨어뜨린다
- 로직이 복잡한 경우 일반 for문을 사용하는 것이 좋다
- 중첩 컴프리헨션은 2단계까지만 권장

---

## 실습 문제

### 실습 1: 점수 → 학점 변환기

`score` 변수에 점수(0~100)를 할당한 후 학점을 출력하세요.

| 점수 범위 | 학점 |
|-----------|------|
| 90 이상 | A |
| 80 이상 | B |
| 70 이상 | C |
| 60 이상 | D |
| 60 미만 | F |

```python
score = 78
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"{score}점은 {grade} 학점입니다.")
```

---

### 실습 2: 짝수/홀수 판별 프로그램

`number` 변수에 숫자를 할당한 후, 짝수인지 홀수인지 판별하세요. 0인 경우도 별도 처리하세요.

```python
number = 7
if number == 0:
    print(f"{number}은(는) 영(제로)입니다.")
elif number % 2 == 0:
    print(f"{number}은(는) 짝수입니다.")
else:
    print(f"{number}은(는) 홀수입니다.")
```

---

### 실습 3: 구구단 출력

```python
dan = 7
print(f"=== {dan}단 ===")
for i in range(1, 10):
    print(f"{dan} x {i} = {dan * i}")
```

---

### 실습 4: 1~100 합계 계산

for문을 사용하여 전체 합계, 짝수 합계, 홀수 합계를 각각 구하세요.

```python
total = 0
even_sum = 0
odd_sum = 0

for i in range(1, 101):
    total += i
    if i % 2 == 0:
        even_sum += i
    else:
        odd_sum += i

print(f"전체 합계: {total}")    # 5050
print(f"짝수 합계: {even_sum}")  # 2550
print(f"홀수 합계: {odd_sum}")   # 2500
```

---

### 실습 5: for문 → 컴프리헨션 변환

아래 3가지 for문을 리스트 컴프리헨션 한 줄로 변환하세요.

```python
# 문제 1: 1~20 중 3의 배수
result1 = [i for i in range(1, 21) if i % 3 == 0]

# 문제 2: 이름 길이 리스트
names = ["김철수", "이영희", "박", "최수진", "정대현"]
result2 = [len(name) for name in names]

# 문제 3: 섭씨 → 화씨 변환
celsius = [0, 10, 20, 30, 40]
result3 = [c * 9/5 + 32 for c in celsius]
```

---

## 핵심 요약

| 주제 | 핵심 키워드 |
|------|-------------|
| **조건문** | `if`, `elif`, `else`, 비교 연산자, 논리 연산자, 삼항 연산자 |
| **반복문** | `for`, `while`, `range()`, `break`, `continue`, `enumerate()` |
| **컴프리헨션** | `[표현식 for 변수 in 시퀀스 if 조건]` |
