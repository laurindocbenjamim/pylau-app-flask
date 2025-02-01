import os
import boto3
from datetime import datetime
from flask import current_app, jsonify, Response
from werkzeug.utils import secure_filename

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="nyc3",
    endpoint_url='https://data-tuning.storage.nyc3.digitaloceanspaces.com',
    aws_access_key_id=os.getenv("SPACE_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SPACE_SECRET_KEY"),
)
timestamp = datetime.now().strftime('%Y%m%d%H%M%S') 

# def upload files
def upload_file(file):
    
    temp_path=os.path.join(current_app.root_path, 'static', 'tmp')
    name_part, extension = os.path.splitext(file.filename)    
    unique_filename = f"{name_part.replace(' ','_').lower()}_{timestamp}{extension}"
    filekey = secure_filename(unique_filename)
    
    try:
        if not os.path.exists(temp_path):
            os.makedirs(temp_path, mode=0o755)

        # Save the file temporarily
        filepath = os.path.join(temp_path, filekey)
        file.save(filepath)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")
        
        client.upload_file(
            filepath,
            current_app.config["BUCKET_NAME"],
            filekey,
            ExtraArgs={"ACL": "public-read"},  # Make the file publicly accessible
        )

        # Remove the file after upload
        os.remove(filepath)
        
        return True, {"status": 200, "message": f"File successfully uploaded into bucket.", "file": filekey}
    except Exception as e:
        return False, {"status": 400, "error": f"Filed to upload file into bucket. [{str(e)}]"}

# def upload files
def upload_file_object(file):

    temp_path=os.path.join(current_app.root_path, 'static', 'tmp')
    name_part, extension = os.path.splitext(file.filename)    
    unique_filename = f"{name_part.replace(' ','_').lower()}_{timestamp}{extension}"
    filekey = secure_filename(unique_filename)
    
    try:
        if not os.path.exists(temp_path):
            os.makedirs(temp_path, mode=0o755)

        # Save the file temporarily
        filepath = os.path.join(temp_path, filekey)
        file.save(filepath)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")
        
        with open(filepath, 'rb') as data:
            client.upload_fileobj(data, current_app.config["BUCKET_NAME"], filekey, ExtraArgs={"ACL": "public-read"})
        
        # Remove the file after upload
        os.remove(filepath)

        return True, {"status": 200, "message": f"File successfully uploaded into bucket.", "file": filekey}
    except Exception as e:
        return False, {"status": 400, "error": f"Filed to upload file into bucket. [{str(e)}]"}

def get_object(filename):
    try:
        response = client.get_object(Bucket='access-key-read-write-1738172573872', Key=filename)
        video_data = response['Body'].read()
        return Response(video_data, mimetype='video/mp4') 

    except Exception as e:
        return f"Error streaming video: {e}"

# Download file
def download_file(filename):
    try:
        # Generate a pre-signed URL for temporary download access
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": 'access-key-read-write-1738172573872', "Key": filename},
            ExpiresIn=60,  # URL expiration time in seconds
        )
        return url, 200
    except Exception as e:
        return str(e), 500
