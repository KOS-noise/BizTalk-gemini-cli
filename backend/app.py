import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 프론트엔드 정적 파일 경로 설정
frontend_folder = os.path.join(os.getcwd(), 'frontend')

app = Flask(__name__, static_folder=frontend_folder)
# 프론트엔드로부터 모든 출처에서의 요청을 허용
CORS(app) 

# Groq 클라이언트 초기화
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables.")
        groq_client = None
    else:
        groq_client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully.")
except Exception as e:
    groq_client = None
    logger.error(f"Error initializing Groq client: {e}")

def get_system_prompt(target):
    """
    대상(target)에 따른 시스템 프롬프트를 생성합니다.
    """
    base_prompt = (
        "당신은 전문적인 비즈니스 커뮤니케이션 컨설턴트입니다. "
        "사용자가 입력한 일상적인 표현을 지정된 대상에 적합한 전문적인 비즈니스 말투로 변환하는 것이 당신의 역할입니다. "
        "다음 규칙을 반드시 준수하세요:\n"
        "1. 원문의 의미를 정확하게 유지하되, 문장의 격식을 높입니다.\n"
        "2. 비즈니스 환경에서 주로 사용하는 용어를 선택합니다.\n"
        "3. 불필요한 사족은 배제하고 간결하고 명확하게 작성합니다.\n"
        "4. 변환된 결과물 텍스트만 출력하세요. 설명이나 추가 멘트는 하지 마세요.\n\n"
    )
    
    if target == "상사":
        target_prompt = (
            "대상: 상사 (Upward)\n"
            "특징: 보고의 명확성, 격식, 신뢰성이 중요합니다.\n"
            "가이드라인:\n"
            "- 정중한 격식체(하십쇼체) 또는 아주 정중한 해요체를 사용하세요.\n"
            "- 결론부터 명확하게 제시하는 보고 형식을 취하세요.\n"
            "- '확인 부탁드립니다', '보고드립니다', '검토 요청드립니다' 등의 표현을 활용하세요."
        )
    elif target == "타팀 동료":
        target_prompt = (
            "대상: 타팀 동료 (Lateral)\n"
            "특징: 협업의 원활함과 요청의 명확성이 중요합니다.\n"
            "가이드라인:\n"
            "- 친절하고 상호 존중하는 어투(해요체)를 사용하세요.\n"
            "- 요청 사항과 원하는 마감 기한을 명확히 전달하는 협조 요청 형식을 취하세요.\n"
            "- '도움 주시면 감사하겠습니다', '확인 부탁드려도 될까요?', '언제까지 가능하실지 확인 부탁드립니다' 등의 표현을 활용하세요."
        )
    elif target == "고객":
        target_prompt = (
            "대상: 고객 (External)\n"
            "특징: 신뢰도, 친절함, 전문성이 중요합니다.\n"
            "가이드라인:\n"
            "- 극존칭을 사용하며 서비스 마인드를 강조하세요.\n"
            "- 안내, 공지, 사과 등 상황에 부합하는 정중한 형식을 사용하세요.\n"
            "- '안내드립니다', '진심으로 사과드립니다', '도움을 드릴 수 있어 기쁩니다' 등의 표현을 활용하세요."
        )
    else:
        target_prompt = "대상에 맞는 정중한 비즈니스 말투로 변환하세요."

    return base_prompt + target_prompt

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    """
    if not groq_client:
        return jsonify({"error": "AI 서비스가 구성되지 않았습니다. API 키를 확인해주세요."}), 500

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        logger.warning(f"Invalid request data: text={original_text}, target={target}")
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    try:
        logger.info(f"Converting text for target: {target}")
        system_prompt = get_system_prompt(target)
        
        completion = groq_client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": original_text}
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        converted_text = completion.choices[0].message.content.strip()
        
        # 가끔 AI가 따옴표를 포함하는 경우 제거
        if converted_text.startswith('"') and converted_text.endswith('"'):
            converted_text = converted_text[1:-1]

        logger.info("Text conversion successful.")
        
        return jsonify({
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        })

    except Exception as e:
        logger.error(f"Error during AI conversion: {e}")
        return jsonify({"error": f"변환 중 서버 오류가 발생했습니다: {str(e)}"}), 500

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # 로컬 테스트용
    app.run(debug=True, port=5000)
