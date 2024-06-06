

import subprocess

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f"Error occurred while executing command: {command}\n{error}")
    else:
        print(f"Output: {output.decode('utf-8')}")

# Git commands
execute_command("git branch")
execute_command("git checkout main")
execute_command("git pull origin main")
execute_command("git merge auth_dev")
# Add here code to resolve conflicts manually
execute_command('git commit -m "Merge dev branch into main"')
execute_command("git push origin main")
#execute_command("git branch -D auth_dev")

# Flask-Migrate commands
#execute_command("flask db init")
execute_command("set FLASK_APP=application.py")
execute_command("python -m flask db stamp")
execute_command("python -m flask db migrate")
execute_command("python -m flask db upgrade")