
# This file is the entry point of the application, it is the file that will be executed by the server
from app import create_application, create_app

# This atribute `app` fits with the heroku's requirements
app = create_app('postgres') # 'postgres'

if __name__ == '__main__':
    app.run()



    