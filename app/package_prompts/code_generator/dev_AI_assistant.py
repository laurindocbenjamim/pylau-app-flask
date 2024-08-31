
import re
# Importing libraries
import openai
import pygame
import time
import os
import traceback
import sys
from openai import OpenAI
# new
from openai import AsyncOpenAI
from ...configs_package.modules.logger_config import get_message as set_logger_message
from ...utils import _catch_sys_except_information


gpt_model = ['gpt-3.5-turbo', 'gpt-4o']


def validate_string_with_digits(s):
    # This pattern allows spaces, accentuated characters, numbers, and common punctuation
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?\'"()]+$'
    if re.match(pattern, s):
        return True
    else:
        return False

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    try:
        client = OpenAI(
        api_key=os.environ['OPEN_AI_API_KEY'],  # this is also the default, it can be omitted
        )
        
        completion = client.chat.completions.create(model=model, messages=messages, temperature=0)
        """ return completion.choices[0].message["content"] """
        return True, completion.choices[0].message.content
    except Exception as e:
        error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="DEV AI Get Completion")
        set_logger_message(error_info)
           
        return False, str(e)