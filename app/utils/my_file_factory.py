
import os
from flask import Request, current_app
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Method to save file 
def upload_file(request_file: Request.files, file_field_name: str):
    """
    This method is used to upload files
    Parameters: 
    => request_file: Request.files is a request files variable that contain a list of files
    => field_name: is the name of the file field
    """
    file = request_file[f'{file_field_name}']
    try:
        #filename = secure_filename(file.filename)

        UPLOAD_FOLDER = f'{current_app.config['UPLOAD_FOLDER']}/tickets'

        # Check if the folder to store the tickets exists, if not, create it
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        #file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Join the file with its path
        filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filename)

        return True
    except Exception as e:
        return False

def validate_file(request: Request, file_field_name):
    # check if the post request has the file part
    if f'{file_field_name}' not in request.files:
        return False, 'No ticket bank part'
        
    file = request.files[f'{file_field_name}']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return False, 'No file has been selected'
        
    if not file:
        return False, "A ticket bank is required"
    if not allowed_file(file.filename):
        return False, "Type file not allowed"
        
    # Return True if everything is okay
    return True, 'OK'
        
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS