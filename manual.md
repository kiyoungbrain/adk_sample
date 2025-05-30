# Google ADK 사용 매뉴얼

## 개요
Google ADK(Agent Development Kit)는 Google의 AI 에이전트를 개발하고 실행하기 위한 도구입니다.

## 설치 방법

1. Python 3.8 이상이 설치되어 있어야 합니다.

2. Gemini API 키 설정
   - Google AI Studio에서 Gemini API 키를 발급받아야 합니다.
   - 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. 가상환경 설정 (권장)
   ```bash
   # 가상환경 생성
   python -m venv .venv

   # 가상환경 활성화
   # Windows:
   .venv\Scripts\Activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

4. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

## 웹 실행 방법 (Shell)

1. 터미널/쉘 실행
   - Windows: PowerShell 또는 Command Prompt 실행
   - macOS/Linux: Terminal 실행

2. 가상환경 활성화 (아직 활성화하지 않은 경우)
   ```bash
   # Windows:
   .venv\Scripts\Activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. 프로젝트 디렉토리로 이동
   ```bash
   cd /path/to/adk_20250507
   ```

4. Dev UI 서버 실행
   ```bash
   adk web
   ```
   - 서버가 시작되면 다음과 같은 메시지가 표시됩니다:
   ```
   Starting ADK web server...
   Server running at http://localhost:8000
   ```

## 주요 기능

## 프로젝트 구조

- `google_search/`: Google Search 내장 에이전트
- `baeminAddress/`: 배민 검색 관련 기능 에이전트
- `filePathControl/`: text.txt 파일 생성 에이전트
- `analytics/`: 데이터 분석 및 시각화 에이전트
- `sampleAgent/`: 샘플 에이전트
- `graphSample/`: 그래프 및 시각화 에이전트