import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.validators import validate_file

def save_uploaded_file(file, file_directory):
    """Handles the uploading and saving of a file."""

    # Define the upload directory within the Flask static folder
    static_dir = os.path.join(current_app.root_path, 'static')
    upload_dir = os.path.join(static_dir, file_directory)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, mode=0o755)

    # Set appropriate file permissions (if necessary)
    os.chmod(upload_dir, 0o755)

    if file and validate_file(file, current_app.config['ALLOWED_EXTENSIONS']):
        # Generate a unique filename using a short UUID and secure the name
        try:
            name_part, extension = os.path.splitext(file.filename)
            short_uuid = str(uuid.uuid4())[:8]
            unique_filename = f"{name_part.replace(' ','_').lower()}_{short_uuid}{extension}"
            filename = secure_filename(unique_filename)

            # Save the file to the upload directory
            file_path=os.path.join(upload_dir, filename)
            file.save(file_path)
            return True, {"message": "File successfully uploaded.", "file_path": file_path}
        except Exception as e:
            return False, {"error": f"Upload filed... {str(e)}"}
    else:
        return False, {"error": "Invalid file format!"}
