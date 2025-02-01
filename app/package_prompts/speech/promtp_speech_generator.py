# Importing the rewquired libraries
import requests
import os

import PyPDF2
from datetime import datetime
from openai import OpenAI

class CreateSpeech(object):
    """
    This class is used to create speed by generating audio from an
    input text.

    In this class we are using the OpenAI API for speech
     
    """
    API_URL = 'https://api.openai.com/v1/audio/speech'
      

    voices = ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')
    formats = ('mp3', 'opus', 'aac', 'flac', 'wav', 'pcm')
    speeds = None
    INPUT_TEXT = None
    MODEL_VOICE = None
    FORMAT = None
    SPEED = None
    FILE_NAME = None
    def __init__(self, input_text, model_voice='alloy', format='mp3', speed=1.0, file_name='speech'):
        """
        COSTRUCTOR PARAMETERS
        
        input_text: is the text from which the audio will be created
        
        model_voice: is the voice used to generate the audio. 
        By default it uses the voice 'alloy'
        but it supports the following voices 
        [alloy, echo, fable, onyx, nova,shimmer]
        
        format: is the output format of the audio. Supported formats 
        (mp3, opus, aac, flac, wav, pcm). 
        By default it retuns an MP3 format
        
        speed: is the speed of the audio generated. 
        it suports speeds from 0.25 to 4.0. By default it uses 1.0 
        
        file_name: It is the name of the audion generated. By default it is 'speech'

        """
        self.INPUT_TEXT = input_text
        self.MODEL_VOICE = model_voice
        self.FORMAT = format
        self.SPEED = speed
        self.FILE_NAME = file_name

    def generate(self):
        """
        This is the audio generator method. It requests the audio using the API URL
        """

        if not self.INPUT_TEXT or self.INPUT_TEXT =='':
            return False, 400, ''
        if not self.MODEL_VOICE or self.MODEL_VOICE =='':
            return False, 400, ''

        try:
            HEADERS = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+ os.environ['OPEN_AI_API_KEY']
            } 
        except KeyError as e:
            print(str(e))
            return False, 400, str(e)
        DATA = {
            "model": "tts-1",
            "input": self.INPUT_TEXT,
            "voice": self.MODEL_VOICE,
            "speed": self.SPEED,
            "format": self.FORMAT
        }
        response = requests.post(self.API_URL, headers=HEADERS, json=DATA)

        directory = "speechs/"

       
        if response.status_code == 200:
            filename = f'{self.FILE_NAME}{datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.{self.FORMAT}'
            # Use the os.path.join to create the full file path
            file_path = os.path.join(directory, filename)

            # Check if the file exists, if true then it create other name for it
            if os.path.exists(file_path):
                print("The file exists.")

            # create the directory  if not exists
            os.makedirs(directory, exist_ok=True)

            with open(file_path, "wb") as file:
                file.write(response.content)
                return True, response.status_code, file_path
        else:
            return False, response.status_code, ''
        
    
    def streaming_speech():
        """
        The Speech API provides support for real time audio streaming using chunk transfer encoding. 
        This means that the audio is able to be played before the full file has been generated and made accessible.
        """        

        client = OpenAI()

        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Hello world! This is a streaming test.",
        )

        #response.stream_to_file("output.mp3")
        response.with_streaming_response.method("output.mp3")

    def extract_content_from_file_v1(file_path):
        """ 
        This metho is used to extract data from a PDF
        """

        if not file_path or '.pdf' not in file_path:
            return  "Invalid format"
        
        if not os.path.exists(file_path):
            return "File not found"
        
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        number_of_pages = len(pdf_reader.pages)
        
        return number_of_pages
    
