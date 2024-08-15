
# This file is the entry point of the application, it is the file that will be executed by the server
from app import create_app

# This atribute `app` fits with the heroku's requirements
# Use test_config={'TESTING': True} to use the test configurations
# Use JDBC='postgres' to use the Development or Production configurations
app = create_app(JDBC='postgres') 
#app = create_app() 

if __name__ == '__main__':
    app.run()



    