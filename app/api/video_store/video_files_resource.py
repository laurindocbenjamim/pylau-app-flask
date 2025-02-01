from flask_restful import Resource
from flask import current_app, request, jsonify
from app.package_code_editor.code_editor_factory import CodeEditorFactory

class VideoFilesResource(Resource):
    def get(self, directory):
        """
        Retrieves a list of video files within a specified directory.

        Args:
            directory (str): The directory path to search for video files.

        Returns:
            jsonify: A JSON response containing the status code, directory path, and list of files.
        """

        editor = CodeEditorFactory(None, None) 
        filelist = editor.load_files(directory=directory)

        if not isinstance(filelist, list):
            return jsonify({"status": 404, "directory": directory, "filelist": ["404", filelist]})

        return jsonify({"status": 200, "directory": directory, "filelist": filelist})