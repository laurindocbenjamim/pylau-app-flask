

from flask.views import View
from flask import render_template, redirect, url_for, jsonify, request
from werkzeug.utils import secure_filename

class SpeechRecognitionView(View):
    methods = ['GET', 'POST']

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self, template) -> None:
        super().__init__()
        self.template =template
    
    def dispatch_request(self):
        
        UPLOAD_FOLDER = 'app/static/uploads/'
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

        if request.method =='GET':
            return render_template(self.template, title="Speech")
        if request.method == 'POST':
            file = request.files['audio']
            #file.save(f"{UPLOAD_FOLDER}{secure_filename(file.filename)}")
            return jsonify({"status": file}, 200)
    

    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS