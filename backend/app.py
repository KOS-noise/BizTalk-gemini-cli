import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# from groq import Groq # Import will be enabled in Phase 3

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS to allow requests from the frontend
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify the backend is running.
    """
    return jsonify({
        "status": "active",
        "service": "BizTone Converter Backend",
        "version": "1.0.0"
    }), 200

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    Main endpoint for text conversion.
    Phase 1: Implements basic structure and dummy response.
    Phase 3: Will integrate actual Groq AI API.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
            
        text = data.get('text', '')
        target = data.get('target', '상사') # Default target
        
        if not text:
            return jsonify({"error": "Text input is required"}), 400

        # TODO: Phase 3 - Implement actual Groq API call here
        # For Phase 1, we return a mock response to validate the flow
        mock_converted_text = f"[TEST] {target}에게 보내는 변환된 메시지: {text}"

        return jsonify({
            "success": True,
            "original_text": text,
            "converted_text": mock_converted_text,
            "target": target
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    # Port can be configured via environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
