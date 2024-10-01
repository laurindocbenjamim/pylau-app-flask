
import json
import os
import stat
from flask import current_app

class StudyNotes(object):

    def check_or_create_file(self,file_path):
        # Check if the folder to store the tickets exists, if not, create it
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path, exist_ok=True)
        except Exception:
            return file_path

    def load_comments(self,file_path):
        """Load comments from a JSON file."""

        file_path = f'{current_app.config['UPLOAD_FOLDER']}/{file_path}'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return []

    def save_comments(self,file_path, comments):
        """Save comments to a JSON file."""
        with open(f'{current_app.config['UPLOAD_FOLDER']}/{file_path}', 'w') as file:
            json.dump(comments, file, indent=4)

    def add_comment(self,file_path, new_comment):
        """Add a new comment to the JSON file."""
         # check if the file path exists if not create it        
        self.check_or_create_file(current_app.config['UPLOAD_FOLDER']+'/user_notes')

        # Set permissions (read, write, execute for owner; read, execute for group and others)
        #os.chmod(current_app.config['UPLOAD_FOLDER']+'/user_notes', 0o755) 
        #os.chmod(current_app.config['UPLOAD_FOLDER']+file_path, 0o644) 
        try:       
            # load the existent comments
            comments = self.load_comments(file_path)

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
            self.save_comments(file_path, comments)
            #os.chmod(file_path, stat.S_IREAD)
            return True, 'OK'
        except Exception as e:
            return False, str(e)


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
