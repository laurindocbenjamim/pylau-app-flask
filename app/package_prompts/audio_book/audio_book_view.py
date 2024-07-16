
from flask.views import View
from flask import render_template, redirect, url_for, request, jsonify
from ..play_speech_content import play_speech, get_all_files

class AudioBookView(View):
    methods=["GET", "POST"]

    def __init__(self, template):
        super().__init__()
        self.template = template

    def dispatch_request(self):

        if request.method == 'GET':
            return render_template(self.template,title="Audio Book", audio_files=[])
        

        if request.method =='POST':
            
            FILE_DIRECTORY="app/static/files/audio_books/"
            files = get_all_files(FILE_DIRECTORY)
            status, resp = play_speech(FILE_DIRECTORY)
            
            return jsonify({'status': status, 'message': resp, 'play_list':files}, 200)
        
    
