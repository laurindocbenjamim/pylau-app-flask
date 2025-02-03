from app.dependencies import request, current_app, jsonify, Resource
from app.api.upload_factory.file_upload import save_uploaded_file  # Import the file upload module


class VideoAnalyzerResource(Resource):
    def post(self):

        #return jsonify({"status":200, "error": "No selected file"})
        # Check if the request contains the file part
        if 'videoFileToAnalyze' not in request.files:
            return jsonify({"status":400, "error": "No video file to analyze has been found!"})

        file = request.files['videoFileToAnalyze']
        
        # Check if a file has been selected
        if file.filename == '':
            return jsonify({"status":400, "error": "No selected file"})

        # Use the save_uploaded_file function from the module
        file_directory=current_app.config['UPLOAD_VIDEO_FOLDER']
        status,result = save_uploaded_file(file, file_directory)
        if not status:
            return jsonify({"status": 400, "error": f"Error: {result}"})
        return jsonify(result)
            
    def get(self):
        # Provide instructions for using the POST method for file upload
        return jsonify({"status":400, "message": "Send a POST request to upload a file."})
