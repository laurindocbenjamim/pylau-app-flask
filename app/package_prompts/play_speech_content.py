import pygame
import time
import os

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
    except Exception as e:
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
