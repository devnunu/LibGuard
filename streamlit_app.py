import streamlit as st
import toml
import os
from typing import Dict, List
from dataclasses import dataclass
import requests
import time
from dotenv import load_dotenv
import json

# .env 파일 로드
load_dotenv()


@dataclass
class LibraryInfo:
    name: str
    current_version: str
    latest_version: str = ""
    is_hotfix: bool = False
    priority: str = "low"
    summary: str = ""
    recommendation: str = ""


class StableLibraryAnalyzer:
    def __init__(self, openai_api_key: str):
        """안정적인 라이브러리 분석기 (직접 HTTP 요청 사용)"""
        self.api_key = openai_api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def call_openai_api(self, messages: List[dict], max_tokens: int = 500) -> str:
        """OpenAI API 직접 호출 (proxies 오류 방지)"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': 0.1
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API 호출 실패: {response.status_code} - {response.text}"

        except Exception as e:
            return f"네트워크 오류: {str(e)}"

    def search_maven_central(self, library_name: str) -> str:
        """Maven Central에서 라이브러리 정보 검색"""
        try:
            search_url = "https://search.maven.org/solrsearch/select"
            params = {
                'q': library_name,
                'rows': 3,
                'wt': 'json'
            }

            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            docs = data.get('response', {}).get('docs', [])

            if not docs:
                return f"'{library_name}'에 대한 검색 결과가 없습니다."

            results = []
            for doc in docs[:2]:
                artifact = f"{doc.get('g', 'unknown')}:{doc.get('a', 'unknown')}"
                latest_version = doc.get('latestVersion', 'unknown')
                results.append(f"- {artifact}: {latest_version}")

            return "Maven Central 검색 결과:\n" + "\n".join(results)

        except Exception as e:
            return f"Maven Central 검색 중 오류: {str(e)}"

    def get_library_info(self, library_name: str, current_version: str) -> str:
        """라이브러리 기본 정보 제공"""
        # 주요 안드로이드 라이브러리들의 최신 정보 (2025년 기준)
        known_libraries = {
            'okhttp': {
                'latest': '4.12.0',
                'info': 'HTTP 클라이언트 라이브러리. 최신 버전에서 보안 패치, 성능 개선, HTTP/3 지원 강화.'
            },
            'retrofit': {
                'latest': '2.9.0',
                'info': 'REST API 클라이언트. 안정적인 버전, 코루틴 지원 개선, 에러 핸들링 강화.'
            },
            'glide': {
                'latest': '4.16.0',
                'info': '이미지 로딩 라이브러리. 메모리 최적화, WebP 지원 개선, 새로운 애니메이션 기능.'
            },
            'gson': {
                'latest': '2.10.1',
                'info': 'JSON 라이브러리. 보안 패치, 성능 개선, null 안전성 강화.'
            },
            'picasso': {
                'latest': '2.8',
                'info': '이미지 로딩 라이브러리. 안정적인 버전, 큰 변경사항 없음.'
            },
            'androidx-core': {
                'latest': '1.12.0',
                'info': 'AndroidX Core 라이브러리. 새로운 API 지원, 호환성 개선.'
            },
            'androidx-appcompat': {
                'latest': '1.6.1',
                'info': 'AppCompat 라이브러리. Material Design 3 지원, 테마 개선.'
            },
            'material': {
                'latest': '1.11.0',
                'info': 'Material Design 라이브러리. Material You 지원, 새로운 컴포넌트 추가.'
            },
            'constraintlayout': {
                'latest': '2.1.4',
                'info': 'ConstraintLayout. 성능 최적화, 새로운 레이아웃 기능.'
            },
            'timber': {
                'latest': '5.0.1',
                'info': '로깅 라이브러리. 안정적인 버전, 성능 개선.'
            }
        }

        lib_key = library_name.lower().replace('-', '').replace('_', '')
        for key, info in known_libraries.items():
            if key.replace('-', '').replace('_', '') in lib_key:
                return f"최신 버전: {info['latest']}, 정보: {info['info']}"

        return f"{library_name}에 대한 기본 정보를 분석 중..."

    def analyze_library(self, lib_name: str, current_version: str) -> LibraryInfo:
        """개별 라이브러리 분석"""
        try:
            # 1. Maven Central에서 정보 수집
            maven_info = self.search_maven_central(lib_name)

            # 2. 기본 라이브러리 정보 수집
            lib_info = self.get_library_info(lib_name, current_version)

            # 3. AI 분석 요청
            messages = [
                {
                    "role": "system",
                    "content": "당신은 안드로이드 라이브러리 업데이트 전문가입니다. 항상 JSON 형식으로 응답하세요."
                },
                {
                    "role": "user",
                    "content": f"""
안드로이드 라이브러리를 분석해주세요.

라이브러리: {lib_name}
현재 버전: {current_version}

수집된 정보:
{maven_info}
{lib_info}

다음 형식으로 JSON 응답해주세요:
{{
    "latest_version": "최신 버전",
    "is_hotfix": true/false,
    "priority": "높음/중간/낮음",
    "summary": "주요 변경사항과 업데이트 권장사항을 한국어로 상세히 요약",
    "recommendation": "업데이트 권장/검토 필요/선택사항"
}}

분석 기준:
- 핫픽스: 패치 버전만 변경 (예: 4.11.0 → 4.11.1)
- 우선순위: 보안 패치 > 버그 수정 > 새 기능 > 문서 업데이트
- 권장사항: 핫픽스는 권장, 메이저 업데이트는 검토 필요
"""
                }
            ]

            # AI API 호출
            ai_response = self.call_openai_api(messages, max_tokens=600)

            # 오류 체크
            if "API 호출 실패" in ai_response or "네트워크 오류" in ai_response:
                return LibraryInfo(
                    name=lib_name,
                    current_version=current_version,
                    summary=ai_response
                )

            try:
                # JSON 파싱 시도
                analysis_data = json.loads(ai_response)

                return LibraryInfo(
                    name=lib_name,
                    current_version=current_version,
                    latest_version=analysis_data.get('latest_version', ''),
                    is_hotfix=analysis_data.get('is_hotfix', False),
                    priority=analysis_data.get('priority', '중간'),
                    summary=analysis_data.get('summary', ''),
                    recommendation=analysis_data.get('recommendation', '')
                )
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 원본 텍스트 사용
                return LibraryInfo(
                    name=lib_name,
                    current_version=current_version,
                    summary=f"AI 분석 결과:\n{ai_response}"
                )

        except Exception as e:
            return LibraryInfo(
                name=lib_name,
                current_version=current_version,
                summary=f"분석 중 예외 발생: {str(e)}"
            )

    def parse_toml_content(self, toml_content: str) -> Dict[str, str]:
        """TOML 내용 파싱"""
        try:
            toml_data = toml.loads(toml_content)
            versions = toml_data.get('versions', {})

            library_versions = {}
            for key, value in versions.items():
                if isinstance(value, str):
                    library_versions[key] = value
                elif isinstance(value, dict) and 'version' in value:
                    library_versions[key] = value['version']

            return library_versions

        except Exception as e:
            raise Exception(f"TOML 파일 파싱 중 오류 발생: {str(e)}")


def main():
    st.set_page_config(
        page_title="📚 LibGuard - 라이브러리 업데이트 분석기",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🛡️ LibGuard - 라이브러리 업데이트 분석기")
    st.markdown("**안드로이드 라이브러리 보안 및 업데이트 관리 도구**")
    st.markdown("---")

    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")

        # OpenAI API 키 처리
        env_api_key = os.getenv('OPENAI_API_KEY')

        if env_api_key:
            st.success("✅ API 키가 .env 파일에서 로드되었습니다")
            openai_api_key = env_api_key
            masked_key = f"sk-...{env_api_key[-4:]}" if len(env_api_key) > 4 else "sk-****"
            st.text(f"사용 중인 키: {masked_key}")
        else:
            st.warning("⚠️ .env 파일에서 OPENAI_API_KEY를 찾을 수 없습니다")
            openai_api_key = st.text_input(
                "OpenAI API Key (수동 입력)",
                type="password",
                placeholder="sk-...",
                help="API 키를 직접 입력하거나 .env 파일에 OPENAI_API_KEY를 설정하세요"
            )

        st.markdown("---")

        # 분석 옵션
        st.header("🔧 분석 옵션")

        max_libraries = st.slider(
            "최대 분석 라이브러리 수",
            min_value=1,
            max_value=20,
            value=3,
            help="비용 절약을 위해 분석할 라이브러리 수를 제한할 수 있습니다"
        )

        analysis_delay = st.slider(
            "분석 간격 (초)",
            min_value=2,
            max_value=10,
            value=4,
            help="API 호출 제한을 피하기 위한 대기 시간"
        )

        st.markdown("---")

        # 샘플 파일 다운로드
        st.header("📄 샘플 파일")

        simple_toml = """[versions]
# 네트워크
okhttp = "4.11.0"
retrofit = "2.9.0"

# 이미지 로딩
glide = "4.15.1"

[libraries]
okhttp = { group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
glide = { group = "com.github.bumptech.glide", name = "glide", version.ref = "glide" }"""

        st.download_button(
            label="📥 심플 테스트 (3개)",
            data=simple_toml,
            file_name="test-simple.toml",
            mime="text/plain",
            help="비용 절약용 - 3개 라이브러리"
        )

        medium_toml = """[versions]
# AndroidX Core
androidx-core = "1.10.1"
androidx-appcompat = "1.6.1"

# Network
okhttp = "4.11.0"
retrofit = "2.9.0"
gson = "2.10.1"

# Image Loading
glide = "4.15.1"
picasso = "2.8"

# UI/Material
material = "1.9.0"
constraintlayout = "2.1.4"

# Logging
timber = "5.0.1"

[libraries]
androidx-core = { group = "androidx.core", name = "core-ktx", version.ref = "androidx-core" }
androidx-appcompat = { group = "androidx.appcompat", name = "appcompat", version.ref = "androidx-appcompat" }
okhttp = { group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
gson = { group = "com.google.code.gson", name = "gson", version.ref = "gson" }
glide = { group = "com.github.bumptech.glide", name = "glide", version.ref = "glide" }
picasso = { group = "com.squareup.picasso", name = "picasso", version.ref = "picasso" }
material = { group = "com.google.android.material", name = "material", version.ref = "material" }
constraintlayout = { group = "androidx.constraintlayout", name = "constraintlayout", version.ref = "constraintlayout" }
timber = { group = "com.jakewharton.timber", name = "timber", version.ref = "timber" }"""

        st.download_button(
            label="📥 중간 테스트 (10개)",
            data=medium_toml,
            file_name="test-medium.toml",
            mime="text/plain",
            help="일반 테스트용 - 10개 라이브러리"
        )

    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📁 TOML 파일 업로드")

        uploaded_file = st.file_uploader(
            "libs.versions.toml 파일을 업로드하세요",
            type=['toml'],
            help="안드로이드 프로젝트의 gradle/libs.versions.toml 파일을 업로드하세요"
        )

        if uploaded_file is not None:
            try:
                toml_content = uploaded_file.read().decode('utf-8')

                with st.expander("📄 업로드된 파일 내용 미리보기"):
                    st.code(toml_content, language='toml')

                if not openai_api_key:
                    st.error("⚠️ OpenAI API 키를 먼저 입력해주세요!")
                    st.stop()

                if st.button("🚀 분석 시작", type="primary"):
                    try:
                        with st.spinner("🔧 분석기 초기화 중..."):
                            analyzer = StableLibraryAnalyzer(openai_api_key)

                        with st.spinner("📖 TOML 파일 파싱 중..."):
                            libraries = analyzer.parse_toml_content(toml_content)

                        st.success(f"✅ {len(libraries)}개의 라이브러리를 발견했습니다!")

                        limited_libraries = dict(list(libraries.items())[:max_libraries])

                        if len(libraries) > max_libraries:
                            st.warning(f"⚠️ 비용 절약을 위해 처음 {max_libraries}개 라이브러리만 분석합니다.")

                        results = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        for i, (lib_name, version) in enumerate(limited_libraries.items()):
                            status_text.text(f"🔍 분석 중: {lib_name} (v{version}) - {i + 1}/{len(limited_libraries)}")

                            result = analyzer.analyze_library(lib_name, version)
                            results.append(result)

                            progress = (i + 1) / len(limited_libraries)
                            progress_bar.progress(progress)

                            if i < len(limited_libraries) - 1:
                                time.sleep(analysis_delay)

                        progress_bar.progress(1.0)
                        status_text.text("✅ 분석 완료!")

                        # 결과 표시
                        st.header("📊 분석 결과")

                        tab1, tab2, tab3 = st.tabs(["📋 요약", "📚 상세 결과", "📝 마크다운 리포트"])

                        with tab1:
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("총 라이브러리", len(results))

                            with col2:
                                hotfix_count = sum(1 for r in results if r.is_hotfix or "핫픽스" in r.summary)
                                st.metric("핫픽스 대상", hotfix_count)

                            with col3:
                                high_priority = sum(1 for r in results if "높음" in str(r.priority))
                                st.metric("높은 우선순위", high_priority)

                        with tab2:
                            for i, result in enumerate(results, 1):
                                with st.expander(f"📦 {i}. {result.name} (v{result.current_version})"):
                                    if result.latest_version:
                                        st.write(f"**최신 버전**: {result.latest_version}")

                                        # 버전 비교 표시
                                        if result.latest_version != result.current_version:
                                            st.write(f"**업데이트 가능**: {result.current_version} → {result.latest_version}")
                                        else:
                                            st.write("**상태**: 최신 버전 사용 중")

                                    if result.priority and result.priority != "low":
                                        priority_color = {"높음": "🔴", "중간": "🟡", "낮음": "🟢"}.get(result.priority, "")
                                        st.write(f"**우선순위**: {priority_color} {result.priority}")

                                    if result.recommendation:
                                        st.write(f"**권장사항**: {result.recommendation}")

                                    if result.is_hotfix:
                                        st.warning("🔥 핫픽스 업데이트 권장!")

                                    st.markdown("**분석 결과**:")
                                    st.markdown(result.summary)

                        with tab3:
                            report = "# 🛡️ LibGuard 라이브러리 업데이트 분석 리포트\n\n"
                            report += f"**분석 일시:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            report += f"**총 라이브러리 수:** {len(results)}개\n\n"

                            # 요약 섹션
                            hotfix_libs = [r for r in results if r.is_hotfix or "핫픽스" in r.summary]
                            high_priority_libs = [r for r in results if "높음" in str(r.priority)]

                            report += "## 🎯 주요 업데이트 권장사항\n\n"

                            if hotfix_libs:
                                report += "### 🔥 즉시 업데이트 권장 (핫픽스)\n"
                                for lib in hotfix_libs:
                                    report += f"- **{lib.name}** ({lib.current_version})\n"
                                report += "\n"

                            if high_priority_libs:
                                report += "### ⚠️ 높은 우선순위 업데이트\n"
                                for lib in high_priority_libs:
                                    report += f"- **{lib.name}** ({lib.current_version})\n"
                                report += "\n"

                            report += "## 📚 상세 분석 결과\n\n"

                            for i, lib in enumerate(results, 1):
                                report += f"### {i}. {lib.name}\n"
                                report += f"**현재 버전:** {lib.current_version}\n"
                                if lib.latest_version:
                                    report += f"**최신 버전:** {lib.latest_version}\n"
                                if lib.priority and lib.priority != "low":
                                    report += f"**우선순위:** {lib.priority}\n"
                                if lib.recommendation:
                                    report += f"**권장사항:** {lib.recommendation}\n"
                                if lib.is_hotfix:
                                    report += f"**핫픽스 여부:** 예 🔥\n"
                                report += f"\n**분석 결과:**\n{lib.summary}\n\n"
                                report += "---\n\n"

                            st.markdown(report)

                            st.download_button(
                                label="📥 리포트 다운로드",
                                data=report,
                                file_name=f"libguard_report_{time.strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )

                    except Exception as e:
                        st.error(f"❌ 분석 중 오류 발생: {str(e)}")
                        st.info("💡 문제가 지속되면 분석 간격을 늘리거나 라이브러리 수를 줄여보세요.")

            except Exception as e:
                st.error(f"❌ 파일 읽기 오류: {str(e)}")

    with col2:
        st.header("ℹ️ 사용 방법")

        st.markdown("""
        ### 📋 단계별 가이드

        1. **API 키 설정**
           - 사이드바에서 OpenAI API 키 확인

        2. **파일 업로드**
           - `libs.versions.toml` 파일 업로드

        3. **분석 옵션 설정**
           - 최대 분석 라이브러리 수 조정
           - 분석 간격 설정 (권장: 4초)

        4. **분석 실행**
           - '분석 시작' 버튼 클릭

        5. **결과 확인**
           - 요약, 상세 결과, 리포트 확인
        """)

        st.markdown("---")

        st.header("🛡️ LibGuard 특징")

        st.markdown("""
        - **안정성**: proxies 오류 완전 해결
        - **보안 중심**: 핫픽스 우선 감지
        - **비용 효율**: 분석 수량 조절
        - **한국어 지원**: 완전 한국어 리포트
        """)

        st.markdown("---")

        st.header("💡 팁")

        st.markdown("""
        - **첫 테스트**: 3개 라이브러리로 시작
        - **분석 간격**: 4초 이상 권장
        - **API 비용**: 라이브러리당 약 $0.02-0.05
        """)


if __name__ == "__main__":
    main()