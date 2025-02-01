
import os, requests
from openai import OpenAI
#os.environ['OPEN_AI_API_KEY']
client = OpenAI(api_key=os.environ.get('DEEP_SEEK_API'), base_url="https://api.deepseek.com")

#print(os.environ.get('DEEP_SEEK_API'))

from flask.views import View
from flask import render_template, redirect, url_for, request, session, json, jsonify
from flask_login import logout_user, login_fresh, login_required
from markupsafe import escape
from flask_wtf.csrf import CSRFProtect
from app.configs_package import csrf, oauth, cache, limiter

from flask import jsonify
from flask.views import MethodView

from openai import OpenAI
from app.models.deep_seek import DeepSeek 

class DeepSeekAPI(MethodView):
    decorators = [limiter.limit("5/minute")]
    #decorators = [login_required]

      # Disable CSRF for this route
    def get(self, id):
        id=escape(id)
        
        #
        def deep_seek_request(model, key):
            deepseek= DeepSeek()
            data = {
                "model": deepseek.get_model(model_category=model, key=key),  # Replace with the exact model name from the docs
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Explain quantum computing in 2 sentences."}
                ],
                "temperature": 0.5,
                "max_tokens": 150
            }

            response = requests.post(deepseek.URL, headers=deepseek.headers, json=data)

            if response.status_code == 200:
                result = response.json()
                return jsonify({"message": result["choices"][0]["message"]["content"], "status_code": f"{response.status_code}"})
            else:
                return jsonify({"error": response.text, "status_code": f"{response.status_code}"})
            
        
        #By using the OpenAI library
        def using_open_ai():
            """
            """
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": "Hello"},
                    ],
                    stream=False
                )
                return jsonify({"message": response,"id": str(id)}), 200
            except Exception as e:
                return jsonify({"error": str(e),"id": str(id)}), 404
        return deep_seek_request("specialized",1)
    #
    def post(self):
        pass
    
   
    def put(self, id):
        pass

    
    def delete(self, id):
        pass

 