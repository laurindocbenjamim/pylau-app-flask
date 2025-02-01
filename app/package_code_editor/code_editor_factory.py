
import json
import os
import glob
import stat
from bs4 import BeautifulSoup
from flask import current_app
from ..utils import sanitize_web_content, sanitize_python_code

class CodeEditorFactory(object):

    myFILE_PATH = myFILE_DIRECTORY = ''

    def __init__(self, file_path,file_directory) -> None:
        self.myFILE_PATH = os.path.join(current_app.root_path, 'static', str(current_app.config['UPLOAD_FOLDER']), str(file_path))
        self.myFILE_DIRECTORY = os.path.join(current_app.root_path, 'static', str(current_app.config['UPLOAD_FOLDER']), str(file_directory)) 


    def list_directories(self, root_directory):
            
        # load all directories
        try:
            _DIRECTORY = os.path.join(current_app.root_path, 'static',str(current_app.config['UPLOAD_FOLDER']), str(root_directory))
            os.chmod(_DIRECTORY, 0o755)
            dirss = os.listdir(_DIRECTORY)

            return True, dirss
        except Exception as e:
            return False, str(e)
        

    def load_file_with_glob(directory):
        """
            Method to load the file's directory
            using the GLOB library

            Args: directory

            Return:
                return a list of files
        
        """
        content = []
        os.chmod(directory, 0o755)
        if directory =='':
            return content
        try:
            
            for file_path in glob.glob(directory):
                with open(file_path, 'r') as file:
                    content.append(file.read())
                return content
        except FileNotFoundError:
            return "Directory not found"
        except Exception as e:
            return f"{str(e)}"

    
    def load_files(self, directory):
        """
        Retrieves a list of filenames within the provided directory.

        Args:
            directory (str): The directory path to search for files.

        Returns:
            list: A list of filenames within the directory.
        """

        # Construct the absolute directory path
        directory_path = os.path.join(current_app.root_path, 'static', str(current_app.config['UPLOAD_FOLDER']), str(directory))

        if not os.path.exists(directory_path):
            return [f"The directory {directory} does not exists!"]
        
        # Set the appropriated permissions
        os.chmod(directory_path, 0o755)
        
        # Check if directory exists
        if not os.path.isdir(directory_path):
            return []  # Return empty list if directory doesn't exist

        # Get list of filenames without reading file content
        return os.listdir(directory_path)
    
    def check_or_create_file(self):
        """
        Description

        Args:


        Return:
        
        
        """
        # Check if the folder to store the tickets exists, if not, create it
        try:
            if not os.path.exists(self.myFILE_DIRECTORY):
                os.makedirs(self.myFILE_DIRECTORY, exist_ok=True)
        except Exception:
            return self.myFILE_DIRECTORY
        
    def create_file(self,filename, encoding='utf-8'):
        """Create a new file"""
         # check if the file path exists if not create it        
        self.check_or_create_file()

        """
       
        """
        script = ""
        if '.htm' in filename: script="""<!-- Write your script below -->"""
        elif '.js' in filename or '.css' in filename: script="""/*--Write your script below--*/"""
        elif '.py' in filename: script="""#-- Write your script below --"""

        resp ="?"
        try:
            # Set read and write permissions for the owner, and read-only for others
            #os.chmod(self.myFILE_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            #os.chmod(self.myFILE_PATH, 0o644)
            #os.chmod(self.myFILE_DIRECTORY, 0o644)
            # Add write permission to the directory
            os.chmod(self.myFILE_DIRECTORY, 0o777)
            if os.path.exists(self.myFILE_PATH):
                resp ='File already exists'
            else:
                with open(self.myFILE_PATH, 'a+') as file:
                    resp = file.write(script)
            # Revoke write privileges
            os.chmod(self.myFILE_DIRECTORY, 0o555)
            #os.chmod(self.myFILE_PATH, 0o444)
            #os.chmod(self.myFILE_DIRECTORY, 0)
            #os.chmod(self.myFILE_DIRECTORY, 0o444)
            return True, resp
        except PermissionError as e:
            # Revoke write privileges
            os.chmod(self.myFILE_DIRECTORY, 0o555)
            #os.chmod(self.myFILE_PATH, 0o444)
            return False, f"Permission denied: {e}"
        except FileNotFoundError as e:
            #os.chmod(self.myFILE_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            #os.chmod(self.myFILE_PATH, 0o644)
            os.chmod(self.myFILE_DIRECTORY, 0o777)
            with open(self.myFILE_PATH, 'a+') as file:
                response = file.write(script)
            # Revoke write privileges
            # Revoke write permission from the directory
            os.chmod(self.myFILE_DIRECTORY, 0o555)
            #os.chmod(self.myFILE_DIRECTORY, 0)
            #os.chmod(self.myFILE_PATH, 0o444)
            return True, f"{str(response)}"
        except Exception as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"{str(e)}"
    

    def load_script(self):
        """Load script from a JSON file."""

        if os.path.exists(self.myFILE_PATH):
            with open(self.myFILE_PATH, 'r') as file:
                return json.load(file)
        return []

    def read_html_file(file_path):
        """
        Reads an HTML file and parses it into a BeautifulSoup object for easy HTML processing.

        Args:
            file_path (str): The path to the HTML file.
        
        Returns:
            Parsed HTML content.
        """

        _FILE_PATH = f'{current_app.config['UPLOAD_FOLDER']}/{file_path}'

        try:

            
            #if os.path.exists(self.myFILE_PATH):
            with open(_FILE_PATH, 'r', encoding='utf-8') as file:
                # Read the entire HTML file content
                html_content = file.read()
            
            soupe = BeautifulSoup(html_content, 'html.parser')
            return soupe.prettify()
        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"An error occurred: {e}"
    
    def read_file(directory,file_path, encoding='utf-8'):
        """
        Reads an HTML file and parses it into a BeautifulSoup object for easy HTML processing.

        Args:
            file_path (str): The path to the HTML file.
        
        Returns:
            Parsed HTML content.
        """

        _FILE_PATH = f'{current_app.config['UPLOAD_FOLDER']}/{file_path}'
        _DIRECTORY = f'{current_app.config['UPLOAD_FOLDER']}/{directory}'
        content =""
        try:

            # Add read and execute permissions for the user, group, and others
            os.chmod(_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            if os.path.exists(_FILE_PATH):
                with open(_FILE_PATH, 'r', encoding=encoding) as file:
                    # Read the entire HTML file content
                    content = file.read()

            # Revoke read and execute permissions for the user, group, and others
            os.chmod(_DIRECTORY, 0)

            #return content
            soupe = BeautifulSoup(content, 'html.parser')
            return soupe.prettify()
        except PermissionError as e:
            # Revoke read and execute permissions for the user, group, and others
            os.chmod(_DIRECTORY, 0)
            return f"Permission denied: {e}"
        except FileNotFoundError:
            # Revoke read and execute permissions for the user, group, and others
            os.chmod(_DIRECTORY, 0)
            return f"File not found: {file_path}"
        except Exception as e:
            # Revoke read and execute permissions for the user, group, and others
            os.chmod(_DIRECTORY, 0)
            return f"An error occurred: {e}"
    

   
    def save_code(self, script):
        """Save script to a JSON file."""

        try:
            # Add read and execute permissions for the user, group, and others
            #os.chmod(self.myFILE_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            # Verify permissions

            #with open(self.myFILE_PATH, 'w') as file:
                #json.dump(script, file, indent=4)
            return True, self.myFILE_DIRECTORY
        except PermissionError as e:
            # Revoke read and execute permissions for the user, group, and others
            os.chmod(self.myFILE_DIRECTORY, 0)
            return f"Permission denied: {e}"
        except FileNotFoundError as e:
            return f"{str(e)}"
        except Exception as e:
            # Revoke read and execute permissions for the user, group, and others
            os.chmod(self.myFILE_DIRECTORY, 0)
            return f"{str(e)}"

    def save_file_script(self, new_script, encoding='utf-8'):
        """Add a new comment to the JSON file."""
         # check if the file path exists if not create it        
        self.check_or_create_file()

        """
        Save the given HTML content to a file.

        Parameters:
        html_content (str): The HTML content to save.
        file_path (str): The path to the file where the HTML content will be saved.
        """

        resp ="?"
        try:
            # Set read and write permissions for the owner, and read-only for others
            os.chmod(self.myFILE_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            os.chmod(self.myFILE_PATH, 0o644)
            #os.chmod(self.myFILE_DIRECTORY, 0o644)
            

            if '.html' in str(self.myFILE_PATH):
                #sanitized_content = sanitize_web_content(new_script)
                with open(self.myFILE_PATH, 'w', encoding=encoding) as file:
                    resp = file.write(new_script)
            elif '.js' in str(self.myFILE_PATH):
                #sanitized_content = sanitize_web_content(new_script)
                with open(self.myFILE_PATH, 'w', encoding=encoding) as file:
                    resp = file.write(new_script)
            elif '.py' in str(self.myFILE_PATH)  or '.css' in str(self.myFILE_PATH):
                # Test with unsafe code
                is_safe, errors = sanitize_python_code(new_script)
                if is_safe:
                    with open(self.myFILE_PATH, 'w') as file:
                        resp = file.write(new_script)
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            #os.chmod(self.myFILE_DIRECTORY, 0)
            #os.chmod(self.myFILE_DIRECTORY, 0o444)
            return True, resp
        except PermissionError as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"Permission denied: {e}"
        except FileNotFoundError as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"{str(e)}"
        except Exception as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"{str(e)}"
    

    def add_update_code(self, new_script):
        """Add a new comment to the JSON file."""
         # check if the file path exists if not create it        
        self.check_or_create_file()

        try:       
            # load the existent script
            script = self.load_script()

            # Update the ID of the script
            if isinstance(script, list):
                if len(script) > 0:
                    last_item = script[-1] if type(script[-1]) is dict else {}
                    if 'id' in last_item.keys():
                        new_script['id'] = 1 + last_item.get('id')
                    else:
                        new_script['id'] = 1
                else:
                    new_script['id'] = 1

            # add and save the new comment
            script.append(new_script)
            self.save_code(script)
            #os.chmod(file_path, stat.S_IREAD)
            return True, 'OK'
        except Exception as e:
            return False, str(e)

    def rename_file(self, new_file_name):
        """ Method to rename the filename """
        try:

            # Set read and write permissions for the owner, and read-only for others
            #os.chmod(self.myFILE_PATH, 0o644)
            # Set read and write permissions for the owner, and read-only for others
            os.chmod(self.myFILE_DIRECTORY, stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            os.chmod(self.myFILE_PATH, 0o644)

            # Rename the file
            os.rename(self.myFILE_PATH, f'{self.myFILE_DIRECTORY}/{new_file_name}')
            
            # Revoke write privileges
            os.chmod(f'{self.myFILE_DIRECTORY}/{new_file_name}', 0o444)

            return True, "OK"
        except PermissionError as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"Permission denied: {e}"
        except FileNotFoundError as e:

            return self.create_file(self.myFILE_PATH)

            # Revoke write privileges
            #os.chmod(self.myFILE_PATH, 0o444)
            #return False, f"{str(e)}"
        except Exception as e:
            # Revoke write privileges
            os.chmod(self.myFILE_PATH, 0o444)
            return False, f"{str(e)}"

    def remove(self,id):
        try:
            # load the existent script
            script = self.load_script()
            # Update the ID of the script
            if isinstance(script, list):
                if len(script) > 0:
                    for key,item in script:
                        if id in item[key]:
                            script.pop(key)
            return True
        except Exception as e:
            return str(e)
    
    def clean_entire_json(self):
        # Open the JSON file in write mode and truncate its content
        with open(self.myFILE_PATH, 'w') as file:
            file.truncate()
""" if len(script) > 0:
                last_item = script[-1]
                if 'id' in last_item:
                    pass
                    #new_comment['id'] = last_item.get('id') + 1
                else:
                    pass
                    new_comment['id'] = 1
            # add and save the new comment
            if isinstance(script, list):
                pass"""

# Example usage
file_path = 'script.json'
new_comment = {
    'user': 'John Doe',
    'comment': 'This is a sample comment.',
    'timestamp': '2024-09-30T17:21:46'
}

#StudyNotes.add_comment(file_path, new_comment)
#print(f"Comment added: {new_comment}")
