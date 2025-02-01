import os
import logging
from pathlib import Path
from flask import session, send_file, current_app, abort, make_response
from flask.views import MethodView
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from app.configs_package import csrf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class FileDownloadResource(MethodView):
    """
    API Resource for secure file downloads
    Supports DOCX, PDF, and CSV files
    """
    
    ALLOWED_EXTENSIONS = {'docx', 'pdf', 'csv'}
    
    def __init__(self):
        self._validate_config()

    def _validate_config(self):
        """Ensure secure configuration with proper directory setup"""
        self.UPLOAD_FOLDER=os.path.join(current_app.root_path,'static', current_app.config['UPLOAD_FOLDER'])
        try:
            # Create directory if it doesn't exist
            Path(self.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
            
            # Verify directory permissions
            if not os.access(self.UPLOAD_FOLDER, os.W_OK):
                raise PermissionError(f"Write access denied to {self.UPLOAD_FOLDER}")
                
            logger.info(f"File storage configured at: {os.path.abspath(self.UPLOAD_FOLDER)}")
            
        except Exception as e:
            logger.critical(f"File storage configuration failed: (Path:  {self.UPLOAD_FOLDER}) error - {str(e)}")
            raise RuntimeError(f"Invalid file storage configuration: (Path:  {self.UPLOAD_FOLDER}) error - {str(e)}")
        
      
    def _is_allowed_file(self, filename):
        """Validate file extension and name"""
        return (
            '.' in filename and
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS and
            secure_filename(filename) == filename
        )

    def _get_mime_type(self, filename):
        """Map file extensions to proper MIME types"""
        extension = filename.rsplit('.', 1)[1].lower()
        return {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'csv': 'text/csv'
        }.get(extension, 'application/octet-stream')

     
    @csrf.exempt
    def get(self, filename):
        """
        Download a file
        ---
        parameters:
          - name: filename
            in: path
            type: string
            required: true
            description: Name of the file to download
        responses:
          200:
            description: File attachment
          400:
            description: Invalid filename
          404:
            description: File not found
          415:
            description: Unsupported file type
        """
        try:
            # Security validation
            if not self._is_allowed_file(filename):
                logger.warning(f"Invalid file request: {filename}")
                abort(400, description=f"Invalid filename format or type {filename}")

            file_path = os.path.join(self.UPLOAD_FOLDER, filename)
            
            if not os.path.isfile(file_path):
                logger.error(f"File not found: {filename}")
                abort(404, description=f"File not found ({file_path}) - [{self.UPLOAD_FOLDER}]")

            # Security headers
            response = make_response(send_file(
                file_path,
                mimetype=self._get_mime_type(filename),
                as_attachment=True
            ))
            
            response.headers.update({
                'X-Content-Type-Options': 'nosniff',
                'Content-Security-Policy': "default-src 'none'",
                'Cache-Control': 'no-store, max-age=0'
            })
            
            return response

        except Exception as e:
            logger.error(f"File download error: {str(e)}", exc_info=True)
            abort(500, description="Internal server error")

