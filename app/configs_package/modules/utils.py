import os


def remove_files_from_root_folder():
    root_folder = os.getcwd()
    files = os.listdir(root_folder)
        
    for file in files:
        file_path = os.path.join(root_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)