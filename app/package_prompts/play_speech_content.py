import pygame
import time
import os
import traceback
import sys

from ..configs_package.modules.logger_config import get_message as set_logger_message

def play_speech(FILE_DIRECTORY):
    if not FILE_DIRECTORY or FILE_DIRECTORY=='':
        return False, "Specify a directory"
    if not os.path.exists(FILE_DIRECTORY):
        return False, "Directory not exists"

    audio_files = get_all_files(FILE_DIRECTORY)

    if len(audio_files) == 0:
        return False, "Empty directory"
    
    try:
        pygame.mixer.init()

        for audio in audio_files:
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                # Wait for the audio file to finish playing
                time.sleep(1)
        
        return True, "Success"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        set_logger_message(f"Error occured on method[play_speech]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
        return False, str(e)


# list of audio files
def get_all_files(FILE_DIRECTORY):
    if not os.path.exists(FILE_DIRECTORY):
        return []
    return [
        f"{FILE_DIRECTORY}{f}"
        for f in os.listdir(FILE_DIRECTORY)
        if os.path.isfile(os.path.join(FILE_DIRECTORY, f))
    ]
