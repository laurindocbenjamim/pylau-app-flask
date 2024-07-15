from flask import Blueprint

bp_ai = Blueprint("ai", __name__, url_prefix="/ai")


from .audio_book.audio_book_view import AudioBookView
bp_ai.add_url_rule("/audio-book", view_func=AudioBookView.as_view("audio_book", "prompts/audio_book.html"))