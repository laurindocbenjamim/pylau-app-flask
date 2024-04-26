#import core

#application = core.create_application()
from flask import Flask, jsonify

application = Flask("Test")
@application.route('/', methods=['GET'])
def home():
    return jsonify({"sms": "Ola mundo"})

if __name__ == '__main__':
    application.run()