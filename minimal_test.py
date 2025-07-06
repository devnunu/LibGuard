# 최소한의 OpenAI 테스트 스크립트
# 호환성 문제 디버깅용

import os
from dotenv import load_dotenv

load_dotenv()


def test_openai_basic():
    """OpenAI 기본 연결 테스트"""
    print("🔧 OpenAI 연결 테스트 시작...")

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return False

    print(f"✅ API 키 확인: {api_key[:10]}...")

    try:
        # 방법 1: 최신 openai 라이브러리 방식
        print("\n📡 방법 1: 최신 OpenAI 라이브러리 테스트")
        import openai

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello! Just testing the connection."}
            ],
            max_tokens=50
        )

        print("✅ 최신 방식 성공!")
        print(f"응답: {response.choices[0].message.content}")
        return True

    except Exception as e1:
        print(f"❌ 최신 방식 실패: {str(e1)}")

        try:
            # 방법 2: 구버전 방식
            print("\n📡 방법 2: 구버전 OpenAI 라이브러리 테스트")
            import openai

            openai.api_key = api_key

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello! Just testing the connection."}
                ],
                max_tokens=50
            )

            print("✅ 구버전 방식 성공!")
            print(f"응답: {response.choices[0].message.content}")
            return True

        except Exception as e2:
            print(f"❌ 구버전 방식도 실패: {str(e2)}")

            # 방법 3: requests로 직접 호출
            try:
                print("\n📡 방법 3: 직접 HTTP 요청 테스트")
                import requests
                import json

                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                }

                data = {
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {'role': 'user', 'content': 'Hello! Just testing the connection.'}
                    ],
                    'max_tokens': 50
                }

                response = requests.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=headers,
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    print("✅ 직접 HTTP 요청 성공!")
                    print(f"응답: {result['choices'][0]['message']['content']}")
                    return True
                else:
                    print(f"❌ HTTP 요청 실패: {response.status_code}")
                    print(f"오류 내용: {response.text}")
                    return False

            except Exception as e3:
                print(f"❌ 직접 HTTP 요청도 실패: {str(e3)}")
                return False


def test_libraries():
    """설치된 라이브러리 버전 확인"""
    print("\n📚 설치된 라이브러리 버전 확인:")

    try:
        import openai
        print(f"✅ openai: {openai.__version__}")
    except:
        print("❌ openai 라이브러리 없음")

    try:
        import streamlit
        print(f"✅ streamlit: {streamlit.__version__}")
    except:
        print("❌ streamlit 라이브러리 없음")

    try:
        import requests
        print(f"✅ requests: {requests.__version__}")
    except:
        print("❌ requests 라이브러리 없음")


if __name__ == "__main__":
    print("🧪 최소한의 OpenAI 테스트")
    print("=" * 50)

    test_libraries()
    success = test_openai_basic()

    print("\n" + "=" * 50)
    if success:
        print("🎉 테스트 성공! 이제 Streamlit 앱을 실행할 수 있습니다.")
    else:
        print("💡 문제 해결 방법:")
        print("1. pip uninstall openai")
        print("2. pip install openai==1.3.0")
        print("3. 다시 테스트 실행")