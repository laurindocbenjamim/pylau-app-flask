

import requests
import os
import stat
import openai
from openai import OpenAI
from flask import request, jsonify
from flask.views import View

# Set your OpenAI API key
#openai.api_key = os.getenv("OPEN_AI_API_KEY") 

class CodeSuggestionOpenAIView(View):

    methods = ['POST']
    API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    def __init__(self):
        pass

    def dispatch_request(self):
      
        """if request.method =='POST':
            
            This is the audio generator method. It requests the audio using the API URL
            

            prompt = request.form.get('prompt')
            
            try:
                HEADERS = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer '+ os.environ['OPEN_AI_API_KEY']
                } 
            except KeyError as e:
                return jsonify({"status": False, "response": str(e)}, 400)
            
            DATA = {
                "prompt": prompt,
                "max_tokens": 50,
                "n": 1,
                "stop": ["\n"]
            }
            response = requests.post(self.API_URL, headers=HEADERS, json=DATA)
        return jsonify({"status": response, "response": response}, 200)"""

        #data = request.json
        prompt = request.form.get('prompt')

        """
         client = OpenAI(
            api_key=os.environ['OPEN_AI_API_KEY'],  # this is also the default, it can be omitted
            )
            
            response = client.chat.completions.create(
                engine="davinci-codex",
                prompt=prompt,
                max_tokens=50
            )
        
        """
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        try:
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=prompt,
                max_tokens=50
            )
            suggestion = response.choices[0].text.strip()
            return jsonify({"suggestion": suggestion})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

                