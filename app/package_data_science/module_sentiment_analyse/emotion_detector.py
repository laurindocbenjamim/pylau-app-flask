

import requests
import traceback
import sys
import os
import re
from flask import current_app, request, Request
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ...configs_package import get_message as set_logger_message
from ibm_watson import ApiException

class EmotionDetector(object):

    def __init__(self) -> None:
        super().__init__()
        

    def validate_form_fields(form = Request.form):
    # Validate each field
   
        if not form.get('comment') or not isinstance(form.get('comment'), str):
            return False
        return True
           

    def validate_only_string(s):
        # This pattern allows spaces, accentuated characters, and common punctuation
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s.,;!?\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
        
    def filter_string(input):
        # This regular expression matches words with or without accentuation and punctuation
        regex = r"[A-Za-zÀ-ÖØ-öø-ÿ.,;?!'\"\s]+"
        result = re.findall(regex, input)
        return ''.join(result) if result else ''
  
    def validate_string_with_digits(s):
        # This pattern allows spaces, accentuated characters, numbers, and common punctuation
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
    
    def emotion_detector(text_to_analyze):
        #web_page_to_analyze = "<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>"
        #text_to_analyze = "Eu odeio voces todos"
        apiKEY =  current_app.config['WATSON_NP_API_KEY']
        apiURL = current_app.config['WATSON_NP_API_URI']        
        natural_language_understanding = None

        try:
            authenticator = IAMAuthenticator(apiKEY)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            natural_language_understanding.set_service_url(apiURL)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"\nJWT Error occured on method[emotion_detector]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False

        
        LANGUAGES = ['en', 'pt'] # Laguages to suport the prediction
        max_score = None
        max_emotion = None
        anger_score = None
        disgust_score = None
        fear_score = None
        joy_score = None
        sadness_score = None
       
        try:
            #Detection with no key-word target
            response = natural_language_understanding.analyze(
                language= LANGUAGES[0],
                html= text_to_analyze,
                features=Features(emotion=EmotionOptions())).get_result()
            
            if response['emotion'] is not None:

                emotions = response['emotion']['document']['emotion']
                max_emotion = max(emotions, key=emotions.get)
                max_score = max(emotions.values())
                anger_score = emotions['anger']
                disgust_score = emotions['disgust']
                fear_score = emotions['fear']
                joy_score = emotions['joy']
                sadness_score = emotions['sadness']
        
        except ApiException as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"\nJWT Error occured on method[emotion_detector]: \n \
                                       ApiException: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"\nJWT Error occured on method[emotion_detector]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            print(f"Method failed with status code {str(ex.code)} '\n' : {ex.message}")
        
        else:
            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': max_emotion,
                'max': max_score
                }