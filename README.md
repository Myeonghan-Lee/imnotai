# ✍️ im-not-ai Web (한글 AI 티 제거기)

AI가 작성한 한국어 텍스트 특유의 어색한 흔적(AI-tell)을 감지하고, 원문의 중요한 정보와 맥락은 그대로 유지하면서 보다 자연스러운 한국어 문체로 다듬어 주는 웹 애플리케이션입니다. 

이 프로젝트는 [Myeonghan-Lee/im-not-ai](https://github.com/Myeonghan-Lee/im-not-ai) 프로젝트의 영감과 교정 가이드라인(Taxonomy)을 기반으로 하며, **Google Gemini API**와 **Streamlit**을 결합하여 브라우저에서 누구나 쉽게 사용할 수 있도록 구현되었습니다.

---

## 🌟 주요 특징

- **의미 불변 (Fidelity First):** 원문의 사실, 데이터 수치, 고유 명사, 직접 인용문 등은 임의로 변형하지 않고 원형대로 보존합니다.
- **근거 기반 (Span-Grounded):** 전체를 새로 쓰지 않고, 번역투나 반복 등 어색함이 탐지된 어구(Span) 중심으로 미세 수정합니다.
- **과윤문 제한 (No Over-Polish):** 설정한 변경 제한 수준(최대 10~50%) 내에서 동작하여 원본의 톤앤매너와 작성자의 개성을 잃지 않도록 돕습니다.
- **구체적인 분석 제공:** 원문에서 수정된 어휘와 그 이유를 한눈에 확인할 수 있도록 상세한 피드백 대시보드를 제공합니다.

---

## 🛠️ 기술 스택

- **Frontend/UI:** Streamlit (Python-based Web UI)
- **AI Engine:** Google Gemini API (`models/gemini-2.5-flash` 또는 `models/gemini-3.5-flash` 등 최신 모델 탑재)
- **Deployment:** Streamlit Community Cloud (GitHub 연동 무료 배포 지원)

---

## 📂 프로젝트 구조

```text
my-im-not-ai-web/
├── app.py              # Streamlit 웹 어플리케이션 소스 코드
├── requirements.txt    # 의존성 패키지 목록
└── README.md           # 프로젝트 가이드라인 (현재 파일)
