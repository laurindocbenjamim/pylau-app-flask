
import json
import os
import stat
from flask import current_app

class StudyNotes(object):

    myFILE_PATH = myFILE_DIRECTORY = ''

    def __init__(self, file_path,file_directory) -> None:
        self.myFILE_PATH = f'{current_app.config['UPLOAD_FOLDER']}/{file_path}'
        self.myFILE_DIRECTORY = f'{current_app.config['UPLOAD_FOLDER']}/{file_directory}' 

    def check_or_create_file(self):
        # Check if the folder to store the tickets exists, if not, create it
        try:
            if not os.path.exists(self.myFILE_DIRECTORY):
                os.makedirs(self.myFILE_DIRECTORY, exist_ok=True)
        except Exception:
            return self.myFILE_DIRECTORY

    def load_comments(self):
        """Load comments from a JSON file."""

        if os.path.exists(self.myFILE_PATH):
            with open(self.myFILE_PATH, 'r') as file:
                return json.load(file)
        return []

    def save_comments(self, comments):
        """Save comments to a JSON file."""
        with open(self.myFILE_PATH, 'w') as file:
            json.dump(comments, file, indent=4)

    def add_comment(self, new_comment):
        """Add a new comment to the JSON file."""
         # check if the file path exists if not create it        
        self.check_or_create_file()

        # Set permissions (read, write, execute for owner; read, execute for group and others)
        #os.chmod(current_app.config['UPLOAD_FOLDER']+'/user_notes', 0o755) 
        #os.chmod(current_app.config['UPLOAD_FOLDER']+file_path, 0o644) 
        try:       
            # load the existent comments
            comments = self.load_comments()

            # Update the ID of the comments
            if isinstance(comments, list):
                if len(comments) > 0:
                    last_item = comments[-1] if type(comments[-1]) is dict else {}
                    if 'id' in last_item.keys():
                        new_comment['id'] = 1 + last_item.get('id')
                    else:
                        new_comment['id'] = 1
                else:
                    new_comment['id'] = 1

            # add and save the new comment
            comments.append(new_comment)
            self.save_comments(comments)
            #os.chmod(file_path, stat.S_IREAD)
            return True, 'OK'
        except Exception as e:
            return False, str(e)

    def remove(self,id):
        try:
            # load the existent comments
            comments = self.load_comments()
            # Update the ID of the comments
            if isinstance(comments, list):
                if len(comments) > 0:
                    for key,item in comments:
                        if id in item[key]:
                            comments.pop(key)
            return True
        except Exception as e:
            return str(e)
    
    def clean_entire_json(self):
        # Open the JSON file in write mode and truncate its content
        with open(self.myFILE_PATH, 'w') as file:
            file.truncate()
""" if len(comments) > 0:
                last_item = comments[-1]
                if 'id' in last_item:
                    pass
                    #new_comment['id'] = last_item.get('id') + 1
                else:
                    pass
                    new_comment['id'] = 1
            # add and save the new comment
            if isinstance(comments, list):
                pass"""

# Example usage
file_path = 'comments.json'
new_comment = {
    'user': 'John Doe',
    'comment': 'This is a sample comment.',
    'timestamp': '2024-09-30T17:21:46'
}

#StudyNotes.add_comment(file_path, new_comment)
#print(f"Comment added: {new_comment}")
