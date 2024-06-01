
#import core.__init__2 as __init__2
from core import create_application

# This atribute `app` fits with the heroku's requirements
app = create_application()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)



    