from app.dependencies import request, current_app, jsonify, Resource
from app.api.storage.repository import upload_file, upload_file_object, download_file, get_object

#@csrf_global.exempt # This Exclude views from protection
class StorageResources(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        sms, status = upload_file(file=file)

        if status==500:
            return jsonify({"message": "Filed uploaded", "status_code": status})
        return jsonify({'message': 'File uploaded successfully', "status_code": status})
    
    def get(self, filename):
        if not filename:
            return jsonify({"error": "Invalide file provided", "status_code": 400})
        
        sms, status_code = get_object(filename=filename)
        if status_code==500:
            return jsonify({"error": "Invalide file provided", "status_code": status_code})
        return jsonify({"message": sms, "status_code": status_code})