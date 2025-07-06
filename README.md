# 🌟 Streamlit 웹 앱 실행 가이드

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성 (보안 권장)
cp .env.example .env
```

### 2. API 키 설정
`.env` 파일을 열어서 API 키를 입력하세요:
```bash
# .env 파일
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. 앱 실행
```bash
# Streamlit 앱 실행
streamlit run streamlit_app.py
```

### 4. 웹 브라우저에서 접속
- 자동으로 브라우저가 열리거나
- 수동으로 `http://localhost:8501` 접속

## 🔐 보안 설정 방법

### 방법 1: .env 파일 사용 (권장)
```bash
# 1. .env 파일 생성
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 2. 앱 실행 (자동으로 .env에서 로드)
streamlit run streamlit_app.py
```

### 방법 2: 환경 변수 사용
```bash
# 1. 환경 변수 설정
export OPENAI_API_KEY="sk-your-key-here"

# 2. 앱 실행
streamlit run streamlit_app.py
```

### 방법 3: 수동 입력 (임시용)
- .env 파일이 없으면 웹 인터페이스에서 직접 입력 가능
- 세션이 종료되면 다시 입력해야 함

## 📱 사용 방법

### 단계 1: API 키 확인
1. 사이드바에서 API 키 상태 확인
2. ✅ 표시가 뜨면 .env에서 자동 로드됨
3. ⚠️ 표시가 뜨면 수동으로 입력 필요

### 단계 2: 파일 업로드
1. **libs.versions.toml** 파일 드래그 앤 드롭
2. 또는 "Browse files" 클릭하여 파일 선택
3. 업로드된 파일 내용 미리보기 확인

### 단계 3: 분석 옵션 설정
- **최대 분석 라이브러리 수**: 비용 절약을 위한 제한
- **분석 간격**: API 호출 제한 방지

### 단계 4: 분석 실행
1. "🚀 분석 시작" 버튼 클릭
2. 진행 상황 실시간 확인
3. 결과를 탭별로 확인

## 🎯 주요 기능

### 📊 실시간 분석 진행률
- 현재 분석 중인 라이브러리 표시
- 전체 진행률 프로그레스 바
- 예상 완료 시간 안내

### 📋 다양한 결과 뷰
1. **요약 탭**: 핵심 통계 정보
   - 총 라이브러리 수
   - 핫픽스 대상 개수
   - 높은 우선순위 항목

2. **상세 결과 탭**: 라이브러리별 분석
   - 접을 수 있는 카드 형태
   - 각 라이브러리의 상세 분석 결과

3. **마크다운 리포트 탭**: 
   - 완전한 리포트 뷰
   - 다운로드 가능한 형태

### 💾 리포트 다운로드
- 마크다운 형식으로 저장
- 타임스탬프가 포함된 파일명
- 팀 공유용으로 활용 가능

## ⚙️ 고급 설정

### 비용 최적화
```python
# 분석 라이브러리 수 제한
max_libraries = 5  # 처음 5개만 분석

# API 호출 간격 조정
analysis_delay = 3  # 3초 대기
```

### 커스터마이징
```python
# 페이지 설정 변경
st.set_page_config(
    page_title="내 회사 라이브러리 분석기",
    page_icon="🏢"
)
```

## 🔧 문제 해결

### 일반적인 문제들

**Q: API 키 오류**
```
A: OpenAI API 키가 유효한지 확인
   - sk-로 시작하는 키인지 확인
   - API 사용량 한도 확인
```

**Q: 파일 업로드 실패**
```
A: TOML 파일 형식 확인
   - .toml 확장자인지 확인
   - 파일 크기가 200MB 미만인지 확인
```

**Q: 분석이 중간에 멈춤**
```
A: 네트워크 연결 상태 확인
   - 인터넷 연결 확인
   - API 호출 제한 확인
```

**Q: 메모리 부족 오류**
```
A: 분석 라이브러리 수 줄이기
   - 최대 10개 이하로 설정
   - 브라우저 새로고침
```

### 디버깅 모드

개발 시 디버깅이 필요하다면:

```bash
# 디버그 모드로 실행
streamlit run streamlit_app.py --logger.level=debug

# 또는 환경 변수 설정
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run streamlit_app.py
```

## 🌐 배포 옵션

### 로컬 네트워크 공유
```bash
# 네트워크의 다른 기기에서 접속 가능
streamlit run streamlit_app.py --server.address=0.0.0.0
```

### Streamlit Cloud 배포
1. GitHub 리포지토리에 코드 업로드
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 앱 배포
3. 팀원들과 링크 공유

### Docker 배포
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📈 성능 최적화

### 캐싱 활용
```python
@st.cache_data
def load_toml_data(file_content):
    return toml.loads(file_content)

@st.cache_resource
def init_analyzer(api_key):
    return LibraryUpdateAnalyzer(api_key)
```

### 세션 상태 관리
```python
# 분석 결과 저장
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
```

## 🎨 UI 커스터마이징

### 테마 설정
`.streamlit/config.toml` 파일 생성:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### CSS 스타일 추가
```python
st.markdown("""
<style>
.stButton > button {
    background-color: #FF4B4B;
    color: white;
}
</style>
""", unsafe_allow_html=True)
```

---

이제 멋진 웹 인터페이스로 라이브러리 분석을 시작해보세요! 🎉

# 🔧 문제 해결 가이드

## 📋 자주 발생하는 오류들

### 1. OpenAI 라이브러리 호환성 오류

**오류 메시지:**
```
validation error for OpenAI
Client.__init__() got an unexpected keyword argument 'proxies'
```

**해결 방법:**
```bash
# 기존 패키지 제거
pip uninstall langchain openai langchain-openai langchain-community

# 최신 호환 버전 설치
pip install langchain==0.1.5 langchain-openai==0.0.6 langchain-community==0.0.20 openai==1.12.0
```

### 2. DuckDuckGo 검색 오류

**오류 메시지:**
```
ImportError: cannot import name 'DuckDuckGoSearchRun' from 'langchain.tools'
```

**해결 방법:**
```bash
# 커뮤니티 패키지에서 import 변경
pip install langchain-community
```

**코드 수정:**
```python
# 기존
from langchain.tools import DuckDuckGoSearchRun

# 수정
from langchain_community.tools import DuckDuckGoSearchRun
```

### 3. API 키 관련 오류

**오류 메시지:**
```
openai.AuthenticationError: Incorrect API key provided
```

**해결 방법:**
1. `.env` 파일 확인:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

2. API 키 유효성 확인:
```bash
# OpenAI 대시보드에서 키 상태 확인
# https://platform.openai.com/api-keys
```

3. 환경 변수 확인:
```python
import os
print(os.getenv('OPENAI_API_KEY'))  # None이면 .env 파일 문제
```

### 4. TOML 파싱 오류

**오류 메시지:**
```
TOML 파일 파싱 중 오류 발생
```

**해결 방법:**
1. TOML 파일 형식 확인:
```toml
[versions]
library-name = "1.0.0"  # 문자열로 감싸기

[libraries]
library-name = { group = "com.example", name = "library", version.ref = "library-name" }
```

2. 특수 문자 확인:
```toml
# 올바른 형식
androidx-core = "1.10.1"

# 잘못된 형식
androidx_core = 1.10.1  # 따옴표 누락
```

### 5. 네트워크 관련 오류

**오류 메시지:**
```
requests.exceptions.ConnectionError
```

**해결 방법:**
1. 인터넷 연결 확인
2. 방화벽/프록시 설정 확인
3. API 호출 간격 늘리기:
```python
time.sleep(5)  # 5초 대기
```

### 6. Memory/Resource 오류

**오류 메시지:**
```
MemoryError or Resource exhausted
```

**해결 방법:**
1. 분석 라이브러리 수 줄이기:
```python
max_libraries = 3  # 3개로 제한
```

2. 분석 간격 늘리기:
```python
analysis_delay = 5  # 5초 대기
```

3. 브라우저 새로고침

## 🛠️ 디버깅 방법

### 1. 상세 로그 활성화

```python
# streamlit_app.py에서 verbose 모드 활성화
self.agent = initialize_agent(
    self.tools,
    self.llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # 디버깅용
)
```

### 2. 단계별 테스트

```python
# 1. API 키 테스트
import openai
client = openai.OpenAI(api_key="your-key")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response)

# 2. TOML 파싱 테스트
import toml
with open("test.toml", "r") as f:
    data = toml.load(f)
print(data)

# 3. 개별 라이브러리 테스트
analyzer = LibraryUpdateAnalyzer("your-key")
result = analyzer.analyze_library("okhttp", "4.11.0")
print(result)
```

### 3. 에러 로그 확인

```bash
# Streamlit 실행 시 로그 확인
streamlit run streamlit_app.py --logger.level=debug

# 또는 Python에서 직접 실행
python -c "
from streamlit_app import LibraryUpdateAnalyzer
analyzer = LibraryUpdateAnalyzer('your-key')
print('Success!')
"
```

## 🔄 완전 초기화 방법

문제가 계속 발생하면 완전히 새로 시작:

```bash
# 1. 가상환경 삭제
rm -rf venv/

# 2. 새 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 재설치
pip install --upgrade pip
pip install -r requirements.txt

# 4. 캐시 삭제
rm -rf ~/.streamlit/
rm -rf __pycache__/

# 5. 앱 재실행
streamlit run streamlit_app.py
```

## 📞 추가 도움

### 1. 라이브러리 버전 확인
```python
import langchain
import openai
import streamlit

print(f"LangChain: {langchain.__version__}")
print(f"OpenAI: {openai.__version__}")
print(f"Streamlit: {streamlit.__version__}")
```

### 2. 환경 정보 확인
```python
import sys
print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")
```

### 3. 최소 동작 테스트
```python
# 최소한의 코드로 동작 확인
import os
from langchain_openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(api_key=api_key)
result = llm.invoke("Hello World")
print(result)
```

---

문제가 해결되지 않으면 구체적인 에러 메시지와 함께 문의해주세요! 🤝