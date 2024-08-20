from flask import Blueprint

bp_ai = Blueprint("ai", __name__, url_prefix="/ai")


from .audio_book.audio_book_view import AudioBookView
bp_ai.add_url_rule("/audio-book", view_func=AudioBookView.as_view("audio_book", "prompts/audio_book.html"))

from .speech.prompt_speech_to_text_generator import ConvertAudioSpeechToText
from .speech.speech_recognition_view import SpeechRecognitionView
bp_ai.add_url_rule("/convert-audio-speech-into-text.html", view_func=SpeechRecognitionView.as_view("speech", "prompts/speech_recognition.html"))

from .speech.stream_assistent import StreamAssistent
# s-laur: means Sidekick/Assistent Laurindo
bp_ai.add_url_rule("/s-laur.html", view_func=StreamAssistent.as_view('st_assistent', 'prompts/stream_assistent.html'))