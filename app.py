from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from main import get_medicine_recommendation

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Serve the main webpage"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    """API endpoint that receives symptoms and returns recommendations"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'Please describe your symptoms'
            }), 400
        
        # Get recommendation from Groq AI
        recommendation, emergency_warning = get_medicine_recommendation(symptoms)
        
        return jsonify({
            'success': True,
            'recommendation': recommendation,
            'emergency': emergency_warning is not None,
            'emergency_warning': emergency_warning
        })
    
    except Exception as e:
        error_msg = str(e)
        
        # Check for API key issues
        if "api_key" in error_msg.lower() or "groq_api_key" in error_msg.lower():
            error_msg = "API key not configured. Please set GROQ_API_KEY environment variable."
        
        return jsonify({
            'success': False,
            'error': f'Error: {error_msg}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    api_key_set = bool(os.environ.get("GROQ_API_KEY"))
    
    return jsonify({
        'status': 'running',
        'model': 'Groq Llama 3.1 70B',
        'api_key_configured': api_key_set,
        'embeddings': 'HuggingFace (free)'
    })

if __name__ == '__main__':
    print("=" * 70)
    print(" 🪐 HEART HEALTH ASSISTANT - CLOUD SERVER")
    print("=" * 70)
    print(" ✓ Server URL: http://localhost:5000")
    print(" ✓ Model: Groq Llama 3.1 70B (FREE)")
    print(" ✓ Embeddings: HuggingFace (FREE)")
    
    if os.environ.get("GROQ_API_KEY"):
        print(" ✓ API Key: Configured ✅")
    else:
        print(" ⚠️  API Key: NOT SET - Get free key from https://console.groq.com")
    
    print(" ✓ Press CTRL+C to stop")
    print("=" * 70)
    
    # Get port from environment (for deployment) or use 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
