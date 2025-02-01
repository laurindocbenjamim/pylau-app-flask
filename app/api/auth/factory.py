
import bleach
from flask import current_app

# Utility Functions
def sanitize_input(input_str):
    return bleach.clean(input_str, strip=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']