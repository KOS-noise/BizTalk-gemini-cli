# BizTone 컨버터 프로젝트 개요

"BizTone 컨버터" 프로젝트는 일상적인 텍스트를 특정 대상(상사, 동료, 고객)에 맞춰 전문적인 비즈니스 언어로 변환하도록 설계된 AI 기반 웹 솔루션입니다. 이 프로젝트는 비즈니스 환경 내에서 커뮤니케이션 효율성과 전문성을 향상시키는 것을 목표로 합니다.

## 프로젝트 구조

이 프로젝트는 프론트엔드와 백엔드 구성 요소를 명확하게 분리하는 모듈형 구조를 따릅니다.

-   **`./` (프로젝트 루트)**: 구성 파일, 문서 (`PRD.md`, `프로그램개요서.md`), 환경 설정 (`.env`, `.env.example`)을 포함합니다.
-   **`backend/`**: Flask 기반의 백엔드 API 서버를 호스팅합니다.
    -   `app.py`: Groq AI API 통합 및 텍스트 변환을 위한 비즈니스 로직을 처리하는 메인 Flask 애플리케이션입니다.
    -   `requirements.txt`: Python 의존성 목록입니다.
-   **`frontend/`**: 사용자 인터페이스를 포함합니다.
    -   `index.html`: 메인 HTML 파일입니다.
    -   `css/style.css`: 주로 Tailwind CSS로 직접 처리되지 않는 특정 애니메이션 및 유틸리티 클래스를 위한 사용자 정의 CSS입니다.
    -   `js/script.js`: API 호출 및 DOM 조작을 위한 클라이언트 측 JavaScript입니다.
-   **`.venv/`**: 의존성 관리를 위한 Python 가상 환경입니다.

## 사용된 기술

-   **프론트엔드**: HTML5, Tailwind CSS, JavaScript (ES6+)
-   **백엔드**: Python, Flask, `python-dotenv`, `Flask-CORS`, `groq` (AI 통합용)
-   **AI 모델**: Groq AI API (`moonshotai/kimi-k2-instruct-0905`)

## 프로젝트 빌드 및 실행

BizTone 컨버터를 설정하고 실행하려면 다음 단계를 따르십시오.

### 1. 환경 설정

1.  **가상 환경 생성 및 활성화**:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
2.  **백엔드 의존성 설치**:
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **API 키 구성**:
    프로젝트 루트 디렉토리 (`.env.example` 옆)에 `.env` 파일을 생성하고 Groq AI API 키를 추가하십시오.
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```
    *올바른 형식은 `.env.example`을 참조하십시오.*

### 2. 백엔드 실행

Flask 개발 서버를 시작합니다.

```bash
.\.venv\Scripts\python.exe backend/app.py
```
서버는 일반적으로 `http://127.0.0.1:5000`에서 실행됩니다. 이 프로세스를 별도의 터미널이나 백그라운드에서 계속 실행하십시오.

### 3. 프론트엔드 실행

웹 브라우저에서 `frontend/index.html` 파일을 엽니다. 프론트엔드는 텍스트 변환을 위해 실행 중인 백엔드에 자동으로 연결됩니다.

## 개발 컨벤션

-   **백엔드 (Python/Flask)**: API 엔드포인트는 `backend/app.py`에 정의됩니다. 더 나은 오류 추적을 위해 로깅이 통합됩니다. 환경 변수는 `python-dotenv`를 사용하여 관리됩니다.
-   **프론트엔드 (HTML/CSS/JS)**: UI는 일반 HTML로 구축되며, 현대적인 미학을 위해 Tailwind CSS(CDN을 통해)로 스타일이 지정되고, 상호 작용 요소는 `js/script.js`의 바닐라 JavaScript로 처리됩니다. 디자인은 반응형이며 다양한 화면 크기에 적응합니다.
-   **AI 통합**: Groq AI 모델에 대한 프롬프트 엔지니어링은 각 대상(상사, 타팀 동료, 고객)에 맞춰 적절한 톤 변환을 보장하도록 맞춤화됩니다.