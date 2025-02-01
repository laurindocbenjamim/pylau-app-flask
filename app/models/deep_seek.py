
import os
from openai import OpenAI

class DeepSeek(object):
    """ 1=> General Chat:

    deepseek-chat

    deepseek-llm

    Example: General Q&A, creative writing, or summarization.
        2=> Code Generation:

    deepseek-coder

    Example: Code writing, debugging, or documentation.
        3=> Specialized Models:

    deepseek-math (if available)

    deepseek-r1 (hypothetical name, confirm via docs)

    Example: Math problem-solving or domain-specific tasks.
    """

    models={"chat": ["deepseek-chat", "deepseek-llm"],
            "code_generation": ["deepseek-coder"],
            "specialized": ["deepseek-math", "deepseek-r1"]
    }

    #os.environ['OPEN_AI_API_KEY']
    API_KEY=os.environ.get('DEEP_SEEK_API')
    URL = "https://api.deepseek.com/v1/chat/completions"
    headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
    
    def get_openai_client(self):
        return OpenAI(api_key=os.environ.get('DEEP_SEEK_API'), base_url="https://api.deepseek.com")

    def get_model(self,*,model_category: str = 'chat',key: int = 0)-> any:
        """ Method to return a DeepSeep model
        params: 
            model_category => Available categories: chat, code_generation and specialized
            key => is a numeric number that specify the type of model into the available categories. 
        return: 
            a model name to be used in a  request method 
        """ 
        return self.models[model_category][key]