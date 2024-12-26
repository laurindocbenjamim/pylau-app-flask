import os
import json
from PIL import Image
from flask import Request, current_app
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "mp4", "webm", "mkv", "avi", "wave"}


def load_content(self, file_type="txt"):
    """Load comments from a JSON file."""

    if file_type == "txt":
        if os.path.exists(self.myFILE_PATH):
            with open(self.myFILE_PATH, "r") as file:
                data = file.read()
                file.close()
                return data
        return []
    elif file_type == "json":
        if os.path.exists(self.myFILE_PATH):
            with open(self.myFILE_PATH, "r") as file:
                data = json.load(file)
                file.close()
                return data
        return []


def read_html_file(file_path):
    """
    Reads an HTML file and parses it into a BeautifulSoup object for easy HTML processing.

    Args:
        file_path (str): The path to the HTML file.

    Returns:
         Parsed HTML content.
    """

    _FILE_PATH = f"{current_app.config['UPLOAD_FOLDER']}/{file_path}"

    try:
        # if not os.path.exists(_FILE_PATH):
        #    return
        with open(_FILE_PATH, "r", encoding="utf-8") as file:
            # Read the entire HTML file content
            html_content = file.read()
            file.close()
            return html_content
    except FileNotFoundError:
        # Open the file in append mode, create if it doesn't exist
        with open(_FILE_PATH, "a+") as file:
            file.write("<pre><h1>Hello, World!</h1></pre>")
        return f"File not found. The file as been created. {_FILE_PATH}"
    except Exception as e:
        return f"An error occurred: {e}"


# Method to save file
def upload_file(request_file: Request.files, file_field_name: str, **kwargs):
    """
    This method is used to upload files
    Parameters:
    => request_file: Request.files is a request files variable that contain a list of files
    => field_name: is the name of the file field
    """
    file = request_file[f"{file_field_name}"]
    try:
        # filename = secure_filename(file.filename)

        UPLOAD_FOLDER = (
            f"{current_app.config['UPLOAD_FOLDER']}/{kwargs.get('folder', 'files')}"
        )

        # Check if the folder to store the tickets exists, if not, create it
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Join the file with its path
        filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filename)
        # Perform file operations
        file.close()

        return True, filename
    except Exception as e:
        return False, str(e)


def validate_image_size(file_path): 
    try: 
        with Image.open(file_path) as img: 
            if img.format not in ['JPEG', 'PNG']: 
                return False 
            if os.path.getsize(file_path) > 2 * 1024 * 1024: # 2MB return False return True except Exception as e: print(e) 
                return False
        return True 
    except Exception as e:  
        return False

def validate_file(request: Request, file_field_name):
    try:
        # check if the post request has the file part
        if f"{file_field_name}" not in request.files:
            return False, f"No {file_field_name} part"

        file = request.files[f"{file_field_name}"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return False, "No file has been selected"

        if not file:
            return False, f"A {file_field_name} is required"
        if not allowed_file(file.filename):
            return False, "Type file not allowed"

        # Return True if everything is okay
        return True, "OK"
    except Exception as e:
        return False, str(e)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_or_create_file(file_path):

    # Check if the folder to store the tickets exists, if not, create it
    if not os.path.exists(f"{current_app.config['UPLOAD_FOLDER']}/{file_path}"):
        os.makedirs(file_path, exist_ok=True)
    return f"{current_app.config['UPLOAD_FOLDER']}/{file_path}"


def saveIntoFile(file_directory: str, data):
    file_path = f"{current_app.config['UPLOAD_FOLDER']}/{file_directory}"

    # Check if the folder to store the tickets exists, if not, create it
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    return True
