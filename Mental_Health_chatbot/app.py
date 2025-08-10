from flask import Flask,request,jsonify
from flask_cors import CORS
from chat_bot_agent import Chatbot  
import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import json
from chat_bot_agent import send_message

api_key = os.environ.get("GROQ_API_KEY")
template = """
Analyze this message for self-harm risk: {message}

Return ONLY this JSON format with no extra text:
{{
  "risk_score": <number 1-10>,
  "trigger_alert": <true if score >= 7, false otherwise>,
  "reason": "<brief reason>"
}}

High risk phrases: "want to die", "kill myself", "hurt myself", "can't handle this", "everything is too much", "giving up", "life is pointless"
"""

prompt = PromptTemplate.from_template(template)
llm = ChatGroq(
    model=os.getenv("model_id"),
    api_key=api_key,
    temperature=0.1
)
chain = prompt | llm 

app = Flask(__name__)

chatbot = Chatbot()
chatbot.template()

if os.environ.get('FLASK_ENV') == 'production':
    CORS(app, resources={r"/chat": {"origins": "https://your-frontend-domain.com"}})
else:
    CORS(app) 
    
@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data:
        return jsonify({"response": "⚠️ Invalid request: No JSON data received."}), 400
    
    user_message = data.get("message")
    if not user_message or not user_message.strip():
        return jsonify({"response": "⚠️ Please provide a message."}), 400
        
    print("usermessage:", user_message)
    selected_lang = data.get("lang", "en")
    
    try:
        response = chatbot.run(user_message, selected_lang)
        
        
        try:
            tracker_result = chain.invoke({"message": user_message})
            content = tracker_result.content.strip()
            
            
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                risk_data = json.loads(json_str)
                
                print(f"Risk assessment: {risk_data}")
                
                if risk_data.get("trigger_alert", False):
                    print(f"⚠️ HIGH RISK ALERT: Score {risk_data.get('risk_score')}")
                    response += "\n\n If you're having thoughts of self-harm, please reach out: Crisis Hotline: 988 | Emergency: 911"
                    send_message()
                    
        except Exception as tracker_error:
            print(f"Tracker error: {tracker_error}")
            print(f"Raw tracker response: {tracker_result.content if 'tracker_result' in locals() else 'No response'}")
        
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"response": "⚠️ An unexpected error occurred on the server. Please try again later."}), 500

@app.route("/", methods=['GET'])
def home():
    return jsonify({"message": "Mental Health Chatbot API is running!"})
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)