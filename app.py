from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemma-3-4b-it:free"

@app.route('/')
def index():
    """Serve the main webpage"""
    return render_template('index.html')

@app.route('/llm-response', methods=['POST'])
def llm_response():
    """
    Endpoint to handle LLM requests
    Accepts JSON with 'message' field
    Returns LLM response
    """
    try:
        # Get the user's message from the request
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Combine user message with the prompt
        full_prompt = f"Answer the following question: {user_message}"
        
        # Prepare the request to OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        }
        
        # Make request to OpenRouter API
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check if request was successful
        if response.status_code == 200:
            response_data = response.json()
            llm_message = response_data['choices'][0]['message']['content']
            return jsonify({'response': llm_message}), 200
        else:
            return jsonify({
                'error': f'OpenRouter API error: {response.status_code}',
                'details': response.text
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # This is for development only
    # In production, use gunicorn
    app.run(host='0.0.0.0', port=6000, debug=True)
