"""import os
from flask import Flask, jsonify


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"sms": "Ola mundo"})

@app.route('/person/<name>', methods=['GET'])
def person(name):
    return  f"My name is {name}"



"""

#import core.__init__2 as __init__2
from core import create_application
"""
app=__init__2.create_application()
if __name__ == '__main__':
    app.run(debug=True)"""

# This atribute `app` fits with the heroku's requirements
app = create_application('postgres')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



    