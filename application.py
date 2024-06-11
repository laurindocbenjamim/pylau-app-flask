

#from core import create_application
from app import create_application

# This atribute `app` fits with the heroku's requirements
app = create_application()

if __name__ == '__main__':
    app.run(debug=True)



    