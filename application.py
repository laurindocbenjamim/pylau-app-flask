
# This file is the entry point of the application, it is the file that will be executed by the server
from app import create_application

# This atribute `app` fits with the heroku's requirements
app = create_application()

if __name__ == '__main__':
    app.run()



    