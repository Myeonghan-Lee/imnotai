import streamlit as st
import json
from google import genai
from google.genai import types

# 1. Streamlit 웹 페이지 설정
st.set_page_config(page_title="한글 AI 티 제거기 (im-not-ai Web)", layout="wide")

st.title("✍️ 한글 AI 티 제거기 (im-not-ai Web)")
st.caption("AI가 쓴 어색한 한국어 문체를 감지하고, 고유 정보는 유지하며 자연스럽게 교정합니다.")

# 2. 사이드바 - 사용자 설정
with st.sidebar:
    st.header("⚙️ 설정 및 API Key")
    # API 키 입력창
    api_key = st.text_input("Google Gemini API Key", type="password", help="Google AI Studio에서 발급받은 API Key를 입력하세요.")
    
    # 사용할 최신 모델 선택 (404 에러 방지를 위해 models/ 접두사 명시)
    model_option = st.selectbox(
        "사용할 Gemini 모델",
        [
            "models/gemini-2.5-flash",
            "models/gemini-3.5-flash",
            "models/gemini-3.1-flash-lite"
        ],
        index=0,
        help="Google API 정책에 맞춰 활성화되어 있는 최신 stable 모델을 사용합니다."
    )
    
    st.markdown("---")
    # 윤문 강도 조절 (과윤문 방지용 타겟값)
    rewrite_intensity = st.slider("최대 변경 비율 제한", min_value=10, max_value=50, value=30, step=5, format="%d%%")
    # 스타일 세부 조정
    target_tone = st.selectbox("타겟 어조 및 장르", ["원본 장르 유지", "비즈니스/공식 보고서 톤", "부드러운 대화체", "에세이/칼럼 톤"])

# 3. im-not-ai 핵심 가이드라인을 담은 시스템 명령어 정의
IM_NOT_AI_SYSTEM_INSTRUCTION = f"""
역할: 전문 한국어 에디터 및 문체 윤문 전문가

[수행 지침]
사용자가 입력한 한글 텍스트에서 AI 특유의 어색한 흔적(번역투, 기계적 병렬, AI 클리셰 등)을 탐색하고, 자연스러운 한국어로 문장 리듬과 문체를 정돈합니다.

[4대 필수 규칙]
1. 의미 불변: 인물, 사실, 주장, 숫자, 직접 인용 등 정보 요소는 100% 원형 그대로 보존해야 합니다.
2. 근거 기반: 문제가 되는 어색한 어구(Span)만 부분 수정하며, 이미 자연스러운 구간은 보존합니다.
3. 장르 유지: 입력 글의 원래 장르 성격을 최대한 존중합니다.
4. 과윤문 제한: 변경율은 {rewrite_intensity}% 수준을 초과하지 않는 한에서 어색함을 지우는 데 집중합니다.

[탐지 및 개선할 주요 패턴 예시]
- 영어 직역/번역투 ('~를 통해', '~에 있어서', '~가 만든') -> 한국어식 주체적 서술형으로 변경.
- 도식적 나열 ('첫째, 둘째, 셋째') -> 문맥에 맞는 매끄러운 연결 문장으로 완화.
- 기계적인 접속사 ('그리고', '하지만', '또한') -> 어미 연결이나 과감한 삭제로 흐름 정돈.
- AI형 상투적 문구 ('결론적으로', '시사하는 바가 크다') -> 불필요할 경우 생략하거나 세련되게 수정.

[출력 약속]
결과는 오직 아래의 JSON 포맷 규칙을 준수하여 출력하십시오:
{{
  "humanized_text": "자연스럽게 다듬어진 전체 결과 텍스트",
  "detected_patterns": [
    {{"pattern": "수정 전 문구", "replacement": "수정 후 문구", "reason": "감지된 AI 어색함 유형 및 수정 사유"}}
  ],
  "change_rate_percentage": 20
}}
"""

# 4. 메인 화면 레이아웃 (좌: 원본 입력 / 우: 다듬어진 결과)
col1, col2 = st.columns(2)

with col1:
    st.subheader("원본 텍스트")
    input_text = st.text_area(
        "AI가 생성하여 다소 어색함이 느껴지는 텍스트를 입력해 주세요.",
        height=400,
        placeholder="예시: 기술의 발전을 통해 우리는 삶을 편리하게 만들 수 있을 것입니다. 첫째로 업무 생산성이 향상되어지며, 둘째로 의사소통에 있어서 어색함이 줄어듭니다. 결론적으로 이는 매우 중대한 변화라 사료되어집니다."
    )

with col2:
    st.subheader("교정 결과")
    result_area = st.empty()

# 5. 실행 로직
if st.button("AI 티 제거하기", type="primary"):
    if not api_key:
        st.error("사이드바에서 Google Gemini API Key를 입력하세요.")
    elif not input_text.strip():
        st.warning("변환할 텍스트를 입력해 주세요.")
    else:
        with st.spinner("한국어 고유의 흐름으로 문체 다듬는 중..."):
            try:
                # google-genai 최신 SDK 기반 클라이언트 선언
                client = genai.Client(api_key=api_key)
                
                # 정형화된 JSON 출력 요구 및 시스템 명령어 전달
                response = client.models.generate_content(
                    model=model_option,  # 사이드바에서 선택된 최신 모델 ID
                    contents=f"아래 텍스트를 개선하십시오. 타겟 스타일: {target_tone}\n\n[대상 텍스트]\n{input_text}",
                    config=types.GenerateContentConfig(
                        system_instruction=IM_NOT_AI_SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        temperature=0.2 # 객관적 일관성을 유지하기 위해 저온도 설정
                    )
                )
                
                # 응답 처리 및 렌더링
                parsed_res = json.loads(response.text)
                humanized = parsed_res.get("humanized_text", "")
                detections = parsed_res.get("detected_patterns", [])
                change_rate = parsed_res.get("change_rate_percentage", 0)
                
                with col2:
                    st.success("자연스러운 교정이 완료되었습니다!")
                    st.markdown("### ✨ 다듬어진 텍스트")
                    st.write(humanized)
                    st.markdown("---")
                    st.metric(label="예상 변경률", value=f"{change_rate}%", delta=f"{rewrite_intensity}% 상한치 대비", delta_color="inverse")
                    
                    if detections:
                        st.markdown("### 🔍 감지된 패턴 및 수정 사항")
                        for item in detections:
                            st.markdown(f"- **`{item.get('pattern')}`** ➡️ **`{item.get('replacement')}`** \n  *({item.get('reason')})*")
                            
            except Exception as e:
                st.error(f"작동 중 오류가 발생했습니다: {e}")
