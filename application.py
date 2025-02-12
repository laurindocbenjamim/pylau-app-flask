
import atexit
import time
from threading import Thread

# This file is the entry point of the application, it is the file that will be executed by the server
from app import create_app

# This atribute `app` fits with the heroku's requirements
# Use test_config={'TSome. boys. love. I don't know how to shoot everybody. You think Muslim? Yes, full dashboard. Fish. Lewis fan. I'm just going to talk. What's yourself? G': True} to use the test configurations
# Use JDBC='postgres' to use the Development or Production configurations
#app = create_app(JDBC='postgres') 
app = create_app(test_config=True) 



# Background task example
def background_task():
    while True:
        print("Running background task...")
        time.sleep(10)

# Start a background thread
#background_thread = Thread(target=background_task)
#background_thread.start()

# Register cleanup function
def cleanup():
    print("Cleaning up before shutdown...")
    #background_thread.join(timeout=1)  # Ensure the background thread is properly terminated

#You can use the atexit module to register cleanup functions that will be called when the interpreter is shutting down
#atexit.register(cleanup)

if __name__ == '__main__':
    #try:
    # flask run --cert=adhoc
    app.run(ssl_context='adhoc', debug=app.config['TESTING'], port=app.config['PORT'])
    #finally:
        # Properly terminate the background thread
    #    background_thread.join()
    



    