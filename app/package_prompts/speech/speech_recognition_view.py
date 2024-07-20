
import os
from pathlib import Path
from flask.views import View
from flask import render_template, redirect, url_for, jsonify, request
from werkzeug.utils import secure_filename

from .prompt_speech_to_text_generator import ConvertAudioSpeechToText

class SpeechRecognitionView(View):
    methods = ['GET', 'POST']

    ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav'}

    def __init__(self,template) -> None:
        super().__init__()
        self.template = template
    
    def dispatch_request(self):
        """
        """
        def allowed_file(filename):
            ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        UPLOAD_FOLDER = 'app/static/uploads/'

        if request.method =='GET':
            return render_template(self.template, title="Speech")
        if request.method == 'POST':
            # check if the post request has the file part
            if 'audio' not in request.files:
                return render_template(self.template, title="Speech", error="No file has been selected", transcription="")    
                    
            file = request.files['audio']
           
            #If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return render_template(self.template, title="Speech", error="No file has been selected", transcription="")   
            
            #file.save(f"{UPLOAD_FOLDER}{secure_filename(file.filename)}")
            filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            file.save(filename)
            
            if not os.path.exists(filename) or not os.path.isfile(filename):
                return render_template(self.template, error="File not found",title="Speech", transcription='')   
    
            convert = ConvertAudioSpeechToText(filename)
            status, transcription = convert.generate_transcription()


            #return jsonify({"filename": convert.FILE_NAME, "status": status, "transcription": transcription})
            return render_template(self.template, title="Speech", transcription=transcription)   
    

        