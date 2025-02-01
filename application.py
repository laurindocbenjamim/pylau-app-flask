
# This file is the entry point of the application, it is the file that will be executed by the server
from app import create_app

# This atribute `app` fits with the heroku's requirements
# Use test_config={'TSome. boys. love. I don't know how to shoot everybody. You think Muslim? Yes, full dashboard. Fish. Lewis fan. I'm just going to talk. What's yourself? G': True} to use the test configurations
# Use JDBC='postgres' to use the Development or Production configurations
#app = create_app(JDBC='postgres') 
app = create_app(test_config=True) 


if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=app.config['TESTING'], port=app.config['PORT'])



    