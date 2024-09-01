
from flask import render_template,request, jsonify, redirect, url_for
from flask.views import View
from .dev_AI_assistant import validate_string_with_digits,get_completion, gpt_model

class DevAiAssistantView(View):
    methods=['GET', 'POST']

    def __init__(self, template) -> None:
        self._template = template
    
    def dispatch_request(self):
        message = ""
        status_code=200
        response=""
        prompt = request.form.get('prompt', None)

        if request.method == 'POST':
            

            if prompt is None:
                message = f"No prompt has been received."
            elif not validate_string_with_digits(prompt):                
                message= f"Invalid prompt"
            else:

                prompt = f""" Read carefull the prompt in brackets 
                [```{prompt}```].
                Check if it is requesting a scripting of a programming language or style sheet languages.
                If true then generate the required script.
                If false return the message in 'Make a request'.

                The structure of your message must be list of a dictionary with the columns named 'message' 
                for a simple message about the code and a column named 'script' for the 
                respective generated code.

                """

                """ 
                The structure of your message must be list of a dictionary with the columns named 'message' 
                for a simple message about the code and a column named 'script' for the 
                respective generated code.
                """

                status, response = get_completion(prompt=prompt, model=gpt_model[0])
                if status:
                    #return [{"entry-point": prompt, "output": response}]
                    message = "Success"
                    status_code=200
            return jsonify({"message": message, "response": response}, status_code)
        
        return render_template(self._template, title="Dev AI", entrypoint=prompt, message=message.replace('`', ''))
        

