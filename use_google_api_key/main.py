import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. .env 파일에서 환경변수 로드
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-lite")
    
    if not api_key or api_key == "your_api_key_here":
        print("에러: .env 파일에 GOOGLE_API_KEY를 설정해주세요.")
        return

    # 2. prompt.md 파일 내용 읽기
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print("에러: prompt.md 파일을 찾을 수 없습니다.")
        return

    # 3. google-genai Client 객체 생성
    client = genai.Client(api_key=api_key)

    # 4. Gemini 모델 호출
    print(f"모델({model_name})에 요청을 보내는 중...\n")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_content
        )
        # 5. 응답 출력
        print("--- 응답 결과 ---")
        print(response.text)
    except Exception as e:
        print(f"API 호출 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
