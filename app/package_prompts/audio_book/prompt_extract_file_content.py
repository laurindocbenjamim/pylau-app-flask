# Importing the rewquired libraries
import requests
import os

import PyPDF2
from datetime import datetime
from pydub import AudioSegment
from openai import OpenAI

class MyExtractorFileContent(object):
    """
    This class is used to create speed by generating audio from an
    input text.

    In this class we are using the OpenAI API for speech
     
    """

    NUMBER_OF_PAGES = 0
    PAGES = None
    
    #
    def extract_from_pdf(self,file_path: str):
        """ 
        This metho is used to extract data from a PDF
        """

        if not file_path or '.pdf' not in file_path:
            return  False, "Invalid format"
        
        if not os.path.exists(file_path):
            return False, "File not found"
        
        try:
            pdf_file = open(file_path, 'rb')

            pdf_reader = PyPDF2.PdfReader(pdf_file)

            number_of_pages = len(pdf_reader.pages)

            self.NUMBER_OF_PAGES = number_of_pages
            self.PAGES = pdf_reader

            return True, number_of_pages
        
        except Exception as e:
            False, str(e)

    #
    def read_page_content(self, page_number: int = 0):
        """
        
        """
        if page_number !=0 and not isinstance(page_number, int):
            return False, "Invalid value for [page_number]"
        try:
            page = self.PAGES.pages[page_number]
            text = page.extract_text()           
            return True,text
        except AttributeError as e:
            False, str(e)
        except IndexError as e:
            return False, "Page number not found"
    

    #  Generate a speech audio
    def generate_audio(input_text: str, output_voice = "alloy", filename:str = 'audio', format: str = ".mp3", speed: int = 1.0, chunk: bool = True, chunk_by:str ='size'):
        """
        This method is used to generate a speech audio from a text  input
        """

        if not input_text:
            return False, "Input text equired"
        
        directory = "files/audio_books/"
        date_now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        date_now_int = str(int(date_now.timestamp()))
        
        ate_now_int = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        
        directory = "files/audio_books/"
        filename = f'{filename}-{date_now_int}'

        chunk_size = 200
        delimiter = "."
        files = []
        if chunk:
            
            chunks = []
            if chunk_by == "size":
                chunks = MyExtractorFileContent.chunk_string_by_size(input_text, chunk_size)
            else:
                chunks = MyExtractorFileContent.chunk_with_by_delimiter(input_text, delimiter)
            for i,chunk in enumerate(chunks):
                
                file_path = os.path.join(directory, f'{filename}_{i}{format}')
                client = OpenAI(
                    api_key=os.environ['OPEN_AI_API_KEY'],  # this is also the default, it can be omitted
                )
                quality = ["tts-1", "tts-1-hd"]
                
                response = client.audio.speech.create(
                    model=quality[0],
                    voice= output_voice,
                    input= chunk,
                    speed= speed
                )

                response.stream_to_file(file_path)
                files.append(file_path)
                #response.with_streaming_response.method()
        else:  
            file_path = os.path.join(directory, f'{filename}{format}')
            client = OpenAI(
                api_key=os.environ['OPEN_AI_API_KEY'],  # this is also the default, it can be omitted
            )
            quality = ["tts-1", "tts-1-hd"]
            
            response = client.audio.speech.create(
                model=quality[0],
                voice= output_voice,
                input= input_text,
                speed= speed
            )

            response.stream_to_file(file_path)
            files.append(file_path)
            #response.with_streaming_response.method()
        
        return True, files
    

    

    #
    def chunk_string_by_size(string, chunk_size):
        return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]
    
    #
    def chunk_with_by_delimiter(string, delimiter):
        return [phrase + delimiter for phrase in string.split(delimiter) if phrase]
    

    
