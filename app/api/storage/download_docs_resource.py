from app.dependencies import request, current_app, jsonify, Resource
from app.api.storage.repository import upload_file, upload_file_object, download_file, get_object

#@csrf_global.exempt # This Exclude views from protection
class DownloadDocsResources(Resource):
    def get(self, filename):
        pass