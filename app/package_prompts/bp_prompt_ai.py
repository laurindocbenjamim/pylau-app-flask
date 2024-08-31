from flask import Blueprint, render_template
from flask_cors import CORS, cross_origin

bp_ai = Blueprint("ai", __name__, url_prefix="/ai")
CORS(bp_ai)


@bp_ai.route('/data-tuning')
@cross_origin(methods=['GET'])
def dashboard_prompt():
    welcome_title = ""
    welcome_message = ""
    return render_template('prompts/overview.html', title="AI Assistant",  welcome_title=welcome_title, welcome_message=welcome_message)

from .audio_book.audio_book_view import AudioBookView
bp_ai.add_url_rule("/audio-book", view_func=AudioBookView.as_view("audio_book", "prompts/audio_book.html"))

from .speech.prompt_speech_to_text_generator import ConvertAudioSpeechToText
from .speech.speech_recognition_view import SpeechRecognitionView
#bp_ai.add_url_rule("/convert-audio-speech-into-text", view_func=SpeechRecognitionView.as_view("speech", "prompts/speech_recognition.html"))
bp_ai.add_url_rule("/convert-audio-speech-into-text", view_func=SpeechRecognitionView.as_view("speech", "prompts/convert-audio-to-text.html"))

from .speech.stream_assistent import StreamAssistent
# s-laur: means Sidekick/Assistent Laurindo
bp_ai.add_url_rule("/s-laur", view_func=StreamAssistent.as_view('stassistent', 'prompts/stream_assistent.html'))

from .code_generator.devAi_assistant_view import DevAiAssistantView
bp_ai.add_url_rule('/dev-ai', view_func=DevAiAssistantView.as_view('devai', 'prompts/code-generator.html'))

