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